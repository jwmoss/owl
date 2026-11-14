# State transitions

This map covers the repository-owned transitions in owl. It does not cover the internal state machines of third-party engines.

## Decision

Keep Ansible as the owner of setup and recovery. Keep systemd as the owner of service lifecycle and GPU exclusion.
Do not add a state-machine library or a second state database.
Use native `block` and `always` tasks for recovery after a failed operation.

A successful setup, an active service, a loaded model, and a correct answer are different states.
Report each state separately. A marker file records an earlier completed task; it does not prove current runtime health.

## State inventory

| Flow and source | States and transition guard | Failure or recovery behavior |
|---|---|---|
| Controller access: `owl-setup` skill, inventory | Unknown → reachable → sudo available. Ansible must reach the configured host. | Stop on access failure. Do not infer access from an inventory file. |
| Host preparation: `roles/base` | Unchecked → sufficient RAM → packages, groups, sudo, linger configured. RAM assertion gates setup. | BIOS changes require the user. Package or privilege errors stop the play. |
| Credentials: `roles/base`, `roles/gufo` | No controller token → anonymous download; token present → protected host copy/download list. | An absent controller token does not remove a previously copied token. |
| ROCm installation: `roles/rocm` | Missing compiler → verified archive → extraction → active symlink → GPU detected. | A compiler path skips extraction. This is not a full installation-integrity check. |
| GPU configuration: `roles/rocm` handlers | File unchanged → no reboot; file changed → initramfs update → reboot → reconnect → GPU check. | An interrupted run after the file write can lose its pending handler notification. |
| Model downloads: `roles/gufo`, `roles/halogen` | Missing/partial → download/resume → checksum verification → usable files. | Retry resumes downloads. Never delete models as a recovery step. |
| Download markers: `roles/gufo` | Revision marker absent → verify/download → marker present → later task skipped. | A marker does not detect later file damage or deletion. |
| Native builds: `roles/maya` | Commit/settings marker absent → build/setup → marker present. | Failed commands do not create the marker. Files may exist after partial setup. |
| Strata bootstrap: `roles/strata` | Executable absent → signed installer; executable present → skip bootstrap. | Existence is only the bootstrap guard. The signed-feed check handles upgrades. |
| Strata upgrade: `roles/strata` | Feed current → no action; update available → stop installed engines → update/test → restore default. | The `always` block attempts restoration on success and task failure. The original failure still propagates. |
| Strata profile: `roles/strata` | Profile absent → launch/download/save → stop temporary server → install service. | An existing profile skips setup even if model, context, or port settings change. |
| Unit configuration: all engine roles | Unit missing/changed → write → daemon reload → enable default → start/restart default. | A changed non-default unit does not restart its running process. |
| Boot selection: all engine roles | Default selected → its unit enabled; other roles disable their units when those roles run. | Changing `default_engine` does not reconcile roles that the user does not run. |
| Runtime switch: unit `Conflicts=` and `owl-wait-memory` | Engine A active → A stops → memory releases → B starts → model loads. | Memory wait times out after about 80 seconds. Systemd retries failures after 30 seconds. |
| Container lifecycle: gufo and halogen units | Image available/pulled → container starts → container stops → container removed. | Images persist. Linger keeps the rootless runtime available after logout. |
| Test selection: `test.yml` | Requested names → installed subset → nonempty assertion → tests. | Missing services are skipped. A nonempty subset can pass without testing every requested name. |
| Readiness and inference: `tests/engine.yml` | Service started → health ready → model listed → chat answered → assertion passes. | Readiness retries are bounded. A chat pass does not prove tool calls, vision, or maximum context. |
| Test cleanup: `test.yml` | Success/failure → attempt default-engine start. | `always` handles ordinary task failures, not lost hosts or controller termination. Starting is not a health check. |
| Release: `.github/workflows` | Conventional commit → release PR → merged version → tag and release. CI separately checks lint/syntax. | CI has no real GPU. A published release is not proof of hardware validation. |

## Evidence and remaining gaps

The Strata update recovery test uses the real service lifecycle through Ansible.
It replaces only the updater command with a deliberate failure.
Before the fix, the default engine stays inactive. After the fix, it is active before test cleanup.
The test must preserve a failing update result; recovery must not turn failure into success.

Other rows describe source behavior. They are not claims that every interruption and failure case has been tested.

Prioritize these remaining transitions separately:

1. Reconcile changed Strata profile settings without rotating or exposing credentials.
2. Distinguish requested engines from the installed subset in test reports without breaking partial-install workflows.
3. Reconcile active non-default engines after binary, model, or unit changes.
4. Verify applied GPU settings after an interrupted configuration/reboot sequence.
5. Verify current artifacts when marker files survive deleted or damaged files.

Each change needs a failing test at its actual interface before implementation.
Avoid combining these changes into one lifecycle rewrite.

## User, developer, and agent contract

- Users receive a specific state and a recovery action, rather than a broad claim that everything works.
- Developers keep one owner per transition and use native Ansible/systemd recovery paths.
- Agents compare desired pins, installed artifacts, active processes, readiness, and inference results separately.
- Agents use Ansible for server inspection, changes, and tests.
- Reports name omitted engines and untested capabilities.
