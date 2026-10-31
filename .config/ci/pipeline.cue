package ci

// One model owns both Forge pipelines. `tools/ci/project.py` renders the
// GitHub workflow and the GitLab pipeline from it; check fails on any drift.

// Owner verification commands, each one native invocation through locked uv.
_checks: [
	{id: "tests", script: "tools/ci/run_tests.py"},
	{id: "schemas", script: "tools/ci/validate_schemas.py"},
	{id: "documents", script: "tools/ci/check_documentation.py"},
	{id: "topology", script: "tools/ci/check_source_topology.py"},
]

_pythonVersions: ["3.12", "3.13", "3.14"]

// The uv release that mise declares; the contract tests hold both projections to it.
_uv: "0.13.6"

// Each GitLab job names one digest-pinned image; the runners allow only these images.
_uvImages: {
	"3.12": "ghcr.io/astral-sh/uv:\(_uv)-python3.12-trixie@sha256:101820b96a31d3438aab226230bc5516d62c6b5b506f0e2d72cb4b6975e27dea"
	"3.13": "ghcr.io/astral-sh/uv:\(_uv)-python3.13-trixie@sha256:b72353db9e2060a798f2920910d453e96370eb0078ba79eee7c3befa90d255fb"
	"3.14": "ghcr.io/astral-sh/uv:\(_uv)-python3.14-trixie@sha256:69acf868b6e856281be85e6088b6e3bde4e46cd83cfd578dbe159076a2920322"
}

_gitleaks: {
	scan:  "gitleaks git --no-banner --redact=100 --exit-code 1 ."
	image: "ghcr.io/gitleaks/gitleaks:v8.30.1@sha256:c00b6bd0aeb3071cbcb79009cb16a60dd9e0a7c60e2be9ab65d25e6bc8abbb7f"
}

// The environment of each locked uv step on GitHub; the setup actions keep their own.
_githubUv: {
	UV_NO_MANAGED_PYTHON:          "1"
	UV_CACHE_DIR:                  "${{ github.workspace }}/build/runtime/tool-cache/uv"
	PIP_DISABLE_PIP_VERSION_CHECK: "1"
}

// GitHub Actions: pinned actions; the Python job runs every owner check on each version.
github: {
	name: "Verify"
	on: {
		push: branches: ["main", "candidate/**"]
		pull_request: branches: ["main"]
		workflow_dispatch: {}
	}
	permissions: contents: "read"
	concurrency: {
		group:                "verify-${{ github.workflow }}-${{ github.ref }}"
		"cancel-in-progress": false
	}
	jobs: {
		"python-contracts": {
			name:      "Python ${{ matrix.python-version }}"
			"runs-on": "ubuntu-24.04"
			strategy: {
				"fail-fast": false
				matrix: "python-version": _pythonVersions
			}
			steps: [
				{
					name: "Check out repository"
					uses: "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1" // v7.0.1
				},
				{
					name: "Set up Python"
					uses: "actions/setup-python@6d4fd22b20465ccc0f7354476588e8df7c9ca0e0" // v7.1.0
					with: "python-version": "${{ matrix.python-version }}"
				},
				{
					name: "Set up uv"
					uses: "astral-sh/setup-uv@68559e99cc807c1eb7e9238fd43a15bba460eec2" // v10.3.3
					with: {
						"enable-cache": true
						version:        _uv
					}
				},
				{
					name: "Report the selected Python"
					env:  _githubUv
					run:  "uv run --locked --python python python --version"
				},
				for check in _checks {
					name: "Run the \(check.id) check"
					env:  _githubUv
					run:  "uv run --locked --python python python \(check.script)"
				},
			]
		}
		security: {
			name:      "Security"
			"runs-on": "ubuntu-24.04"
			steps: [
				{
					name: "Check out repository"
					uses: "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1" // v7.0.1
					with: "fetch-depth": 0
				},
				{
					name: "Run the pinned Gitleaks action"
					uses: "gitleaks/gitleaks-action@e0c47f4f8be36e29cdc102c57e68cb5cbf0e8d1e" // v3.0.0
					env: {
						GITHUB_TOKEN:     "${{ secrets.GITHUB_TOKEN }}"
						GITLEAKS_VERSION: "8.30.1"
					}
				},
				{name: "Report the Gitleaks version", run: "gitleaks version"},
				{name: "Run the repository security command", run: _gitleaks.scan},
			]
		}
	}
}

// GitLab: ref protection selects the project's protected or review runner (DR-0003).
// Explicit runtime Firecrawl validation is omitted from hosted CI: it needs reviewed
// local images and must prove loopback teardown rather than borrow shared runner state.
gitlab: {
	workflow: rules: [
		{if: "$CI_PIPELINE_SOURCE != \"push\" && $CI_PIPELINE_SOURCE != \"web\"", when: "never"},
		{if: "$CI_COMMIT_REF_PROTECTED == \"true\"", variables: WIB_CI_RUNNER_TAG: "ci-linux-arm64-container-protected"},
		{variables: WIB_CI_RUNNER_TAG: "ci-linux-arm64-container"},
	]
	stages: ["verify"]
	default: tags: ["$WIB_CI_RUNNER_TAG"]
	".python-contracts": {
		stage: "verify"
		variables: {
			UV_PYTHON_DOWNLOADS: "never"
			UV_CACHE_DIR:        "/cache/uv"
			UV_LINK_MODE:        "copy"
			// The CI host's network drops some long downloads; uv retries them inside the job.
			UV_HTTP_RETRIES:         "10"
			UV_HTTP_TIMEOUT:         "120"
			UV_CONCURRENT_DOWNLOADS: "8"
		}
		script: [for check in _checks {"uv run --locked --python \"python${PYTHON_VERSION}\" python \(check.script)"}]
	}
	"python 3.12": {
		extends: ".python-contracts"
		image:   _uvImages["3.12"]
		variables: PYTHON_VERSION: "3.12"
	}
	"python 3.13": {
		extends: ".python-contracts"
		image:   _uvImages["3.13"]
		variables: PYTHON_VERSION: "3.13"
	}
	"python 3.14": {
		extends: ".python-contracts"
		image:   _uvImages["3.14"]
		variables: PYTHON_VERSION: "3.14"
	}
	security: {
		stage: "verify"
		image: {
			name: _gitleaks.image
			entrypoint: [""]
		}
		variables: GIT_DEPTH: "0"
		script: [
			"git config --global --add safe.directory \"$CI_PROJECT_DIR\"",
			"gitleaks version",
			_gitleaks.scan,
		]
	}
}
