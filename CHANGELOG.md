# Changelog

## [3.9.0](https://github.com/jwmoss/owl/compare/v3.8.0...v3.9.0) (2026-11-27)


### Features

* **engines:** update ghcr.io/peonist-ai/halogen-flash-server docker tag to v0.21.0 ([#110](https://github.com/jwmoss/owl/issues/110)) ([07fa2b5](https://github.com/jwmoss/owl/commit/07fa2b59543df505b114ceae4480e17ad798286e))
* **engines:** update https://huggingface.co/peonist-ai/halogen-qwen3.8-flash-next digest to 3842e10 ([#109](https://github.com/jwmoss/owl/issues/109)) ([f111495](https://github.com/jwmoss/owl/commit/f1114952526dac2cb6dd740f1ec825d989a941c6))

## [3.8.0](https://github.com/jwmoss/owl/compare/v3.7.0...v3.8.0) (2026-11-26)


### Features

* **strata:** set up a preset again when its context changes; 256K default ([d2031e6](https://github.com/jwmoss/owl/commit/d2031e659f03bc913e010ac7c60f5631a1c1931b))


### Bug Fixes

* **halogen:** remove the halogen images that are not pinned ([d2031e6](https://github.com/jwmoss/owl/commit/d2031e659f03bc913e010ac7c60f5631a1c1931b))
* **maya:** use Maya's own GPU memory reserve, with 16384 for DeepSeek ([d2031e6](https://github.com/jwmoss/owl/commit/d2031e659f03bc913e010ac7c60f5631a1c1931b))
* **rocm:** stop background memory compaction that pauses the GPU ([d2031e6](https://github.com/jwmoss/owl/commit/d2031e659f03bc913e010ac7c60f5631a1c1931b))

## [3.7.0](https://github.com/jwmoss/owl/compare/v3.6.0...v3.7.0) (2026-11-26)


### Features

* **engines:** update dependency mw00/project-maya to v1.1.78 ([#99](https://github.com/jwmoss/owl/issues/99)) ([2ea73db](https://github.com/jwmoss/owl/commit/2ea73db93c8f2db67149192dd240928017fe3554))
* **engines:** update dependency mw00/project-maya to v1.1.81 ([#101](https://github.com/jwmoss/owl/issues/101)) ([2875e23](https://github.com/jwmoss/owl/commit/2875e23fd41b5f4dc9a58c9e6131c34be807f7de))
* **engines:** update dependency niko1221/strata to v0.2.21 ([#100](https://github.com/jwmoss/owl/issues/100)) ([a15d3b3](https://github.com/jwmoss/owl/commit/a15d3b3b414a9ba2ebf60dcda705a251a8af29af))
* **engines:** update dependency niko1221/strata to v0.2.22 ([#103](https://github.com/jwmoss/owl/issues/103)) ([72e2b29](https://github.com/jwmoss/owl/commit/72e2b29699c04d1516b0c77b445bf8287c61f69a))
* **engines:** update https://huggingface.co/peonist-ai/halogen-qwen3.8-flash-next digest to fe3653f ([#98](https://github.com/jwmoss/owl/issues/98)) ([457631d](https://github.com/jwmoss/owl/commit/457631dab7591eb41c54b96cfe0887b4a81f95d2))
* **maya:** hard-link identical model files across Maya models ([#97](https://github.com/jwmoss/owl/issues/97)) ([b19e50c](https://github.com/jwmoss/owl/commit/b19e50c6886fa31e487563da9422ff495760aab5))


### Bug Fixes

* **model_cache:** retry a store copy that NFS stops ([e93e438](https://github.com/jwmoss/owl/commit/e93e438688782f8cb213d54384604a8a642f1664))
* Strata preset folders, engine switch race and stale store mount ([#94](https://github.com/jwmoss/owl/issues/94)) ([039b378](https://github.com/jwmoss/owl/commit/039b3784a5677da3356d95bd74d5bc91c26c88a6))

## [3.6.0](https://github.com/jwmoss/owl/compare/v3.5.0...v3.6.0) (2026-11-24)


### Features

* **engines:** update dependency mw00/project-maya to v1.1.77 ([#92](https://github.com/jwmoss/owl/issues/92)) ([bacece2](https://github.com/jwmoss/owl/commit/bacece2d911479bcd302949269a16f1ce0e1685c))

## [3.5.0](https://github.com/jwmoss/owl/compare/v3.4.0...v3.5.0) (2026-11-23)


### Features

* **engines:** update dependency mw00/project-maya to v1.1.74 ([#89](https://github.com/jwmoss/owl/issues/89)) ([97e44fd](https://github.com/jwmoss/owl/commit/97e44fd36272abad03f8cf1adcff2f60c4d1c2e5))
* **engines:** update dependency niko1221/strata to v0.2.20 ([#91](https://github.com/jwmoss/owl/issues/91)) ([46e9d18](https://github.com/jwmoss/owl/commit/46e9d18c7ff2ab7093c24fda07f1f90208b77211))

## [3.4.0](https://github.com/jwmoss/owl/compare/v3.3.0...v3.4.0) (2026-11-22)


### Features

* **engines:** update dependency mw00/project-maya to v1.1.70 ([#84](https://github.com/jwmoss/owl/issues/84)) ([bd0ff71](https://github.com/jwmoss/owl/commit/bd0ff7160b89ce5a126a67baec69efa4efa8135c))
* **engines:** update dependency mw00/project-maya to v1.1.72 ([#87](https://github.com/jwmoss/owl/issues/87)) ([2336028](https://github.com/jwmoss/owl/commit/2336028cba3476c5ca028b401f5c7683bacbe506))
* **engines:** update dependency niko1221/strata to v0.2.17 ([#85](https://github.com/jwmoss/owl/issues/85)) ([5bd0165](https://github.com/jwmoss/owl/commit/5bd0165099c4ad4ca670bed59c5619a13ab367ee))
* **engines:** update dependency niko1221/strata to v0.2.18 ([#88](https://github.com/jwmoss/owl/issues/88)) ([295078f](https://github.com/jwmoss/owl/commit/295078f0a09f140a2d89b2d224b3e7b6fbd91bd3))

## [3.3.0](https://github.com/jwmoss/owl/compare/v3.2.0...v3.3.0) (2026-11-19)


### Features

* **engines:** update dependency mw00/project-maya to v1.1.68 ([#82](https://github.com/jwmoss/owl/issues/82)) ([8cba12b](https://github.com/jwmoss/owl/commit/8cba12b2391eeba3f13997eaa06df2e1217a8585))
* **engines:** update dependency niko1221/strata to v0.2.16 ([#81](https://github.com/jwmoss/owl/issues/81)) ([32734ef](https://github.com/jwmoss/owl/commit/32734ef07fcad2bdc704cd88661832c773b03fa7))

## [3.2.0](https://github.com/jwmoss/owl/compare/v3.1.0...v3.2.0) (2026-11-18)


### Features

* **engines:** update dependency mw00/project-maya to v1.1.67 ([#77](https://github.com/jwmoss/owl/issues/77)) ([8964671](https://github.com/jwmoss/owl/commit/8964671b882cc728d5c4f871468fafefe9548364))
* **engines:** update ghcr.io/peonist-ai/halogen-flash-server docker tag to v0.20.7 ([#78](https://github.com/jwmoss/owl/issues/78)) ([8f99a90](https://github.com/jwmoss/owl/commit/8f99a90d48b08a7117ad4d91c5fad0e83f408e4e))
* **engines:** update https://huggingface.co/peonist-ai/halogen-qwen3.8-flash-next digest to 05ec74b ([#76](https://github.com/jwmoss/owl/issues/76)) ([7cd17d9](https://github.com/jwmoss/owl/commit/7cd17d96d594664cb65434aa3bb2416105426c80))


### Bug Fixes

* **halogen:** download the ht4 draft head that 0.20.7 uses ([#80](https://github.com/jwmoss/owl/issues/80)) ([a0ef3b7](https://github.com/jwmoss/owl/commit/a0ef3b79f0b5f77fab522bbe41948eeb400b90e4))

## [3.1.0](https://github.com/jwmoss/owl/compare/v3.0.0...v3.1.0) (2026-11-18)


### Features

* **engines:** update dependency mw00/project-maya to v1.1.66 ([#73](https://github.com/jwmoss/owl/issues/73)) ([fe8d93d](https://github.com/jwmoss/owl/commit/fe8d93d69ddfa9a91e03f34b7ed3d83db02c0ca4))
* **engines:** update dependency niko1221/strata to v0.2.15 ([#71](https://github.com/jwmoss/owl/issues/71)) ([2906a4c](https://github.com/jwmoss/owl/commit/2906a4cbb8bbe459593183959bf0c2b72f30a576))
* **engines:** update ghcr.io/peonist-ai/halogen-flash-server docker tag to v0.20.6 ([#72](https://github.com/jwmoss/owl/issues/72)) ([95f71a2](https://github.com/jwmoss/owl/commit/95f71a29648bdd9e5313432c9495f4d27857c65f))
* **engines:** update https://huggingface.co/peonist-ai/halogen-qwen3.8-flash-next digest to 5c72aef ([#70](https://github.com/jwmoss/owl/issues/70)) ([df5a251](https://github.com/jwmoss/owl/commit/df5a251352802287c176b2a066f57aa9058e1a92))

## [3.0.0](https://github.com/jwmoss/owl/compare/v2.3.0...v3.0.0) (2026-11-16)


### ⚠ BREAKING CHANGES

* serve every engine on one port, with HTTPS through Tailscale Serve ([#67](https://github.com/jwmoss/owl/issues/67))

### Features

* serve every engine on one port, with HTTPS through Tailscale Serve ([#67](https://github.com/jwmoss/owl/issues/67)) ([6800e32](https://github.com/jwmoss/owl/commit/6800e3260750da2d6555bdc61c97ea45ac61f569))
* switch the default engine with engine.yml, fall back to it on failure ([#68](https://github.com/jwmoss/owl/issues/68)) ([b2bb746](https://github.com/jwmoss/owl/commit/b2bb74609555ae4c2a4268265a1c1d79232ee208))

## [2.3.0](https://github.com/jwmoss/owl/compare/v2.2.0...v2.3.0) (2026-11-16)


### Features

* **engines:** update dependency mw00/project-maya to v1.1.65 ([#65](https://github.com/jwmoss/owl/issues/65)) ([b244800](https://github.com/jwmoss/owl/commit/b244800ccfea8adf31617a59463c5874fbb30923))
* **engines:** update https://huggingface.co/peonist-ai/halogen-qwen3.8-flash-next digest to e3b33d6 ([#64](https://github.com/jwmoss/owl/issues/64)) ([040575e](https://github.com/jwmoss/owl/commit/040575e34d46a56c35c44b714523de69a10637bc))

## [2.2.0](https://github.com/jwmoss/owl/compare/v2.1.0...v2.2.0) (2026-11-16)


### Features

* **halogen:** read pictures with the vision file by default ([#62](https://github.com/jwmoss/owl/issues/62)) ([72e04cb](https://github.com/jwmoss/owl/commit/72e04cb9e148a8bb001da344eae84f314d2fe284))

## [2.1.0](https://github.com/jwmoss/owl/compare/v2.0.0...v2.1.0) (2026-11-15)


### Features

* **engines:** update dependency mw00/project-maya to v1.1.64 ([#58](https://github.com/jwmoss/owl/issues/58)) ([584fc65](https://github.com/jwmoss/owl/commit/584fc658e24cbb1539fc6c62cbfdcdbb15dff4b0))
* **engines:** update dependency niko1221/strata to v0.2.14 ([#59](https://github.com/jwmoss/owl/issues/59)) ([73424bd](https://github.com/jwmoss/owl/commit/73424bdea70180d634a489f49618e9ac058b5f89))
* **engines:** update ghcr.io/peonist-ai/halogen-flash-server docker tag to v0.20.5 ([#60](https://github.com/jwmoss/owl/issues/60)) ([2ad60ac](https://github.com/jwmoss/owl/commit/2ad60acbf489237691e3c2893ebec89430c9c607))
* **engines:** update https://huggingface.co/peonist-ai/halogen-qwen3.8-flash-next digest to 95a013d ([#57](https://github.com/jwmoss/owl/issues/57)) ([6dfeb58](https://github.com/jwmoss/owl/commit/6dfeb58e025da417bf8cab217e032765577569c4))

## [2.0.0](https://github.com/jwmoss/owl/compare/v1.6.0...v2.0.0) (2026-11-14)


### ⚠ BREAKING CHANGES

* libosmos.yml, gufo.yml, their services and the minimax Maya model are gone. strata_model is replaced by strata_presets and strata_preset. Model files move from ~/Models to ~/models.

### Features

* **engines:** update dependency mw00/project-maya to v1.1.62 ([#53](https://github.com/jwmoss/owl/issues/53)) ([3cfdd44](https://github.com/jwmoss/owl/commit/3cfdd4436de745c58c05a501425924bf4b74c7c0))
* **engines:** update dependency mw00/project-maya to v1.1.63 ([#56](https://github.com/jwmoss/owl/issues/56)) ([40f92ac](https://github.com/jwmoss/owl/commit/40f92ac0caaf0834ff771d7c2ae604d9de5d94e9))
* serve GLM and DeepSeek on Maya, add an NFS model store, remove libosmos and gufo ([#51](https://github.com/jwmoss/owl/issues/51)) ([b2b0b17](https://github.com/jwmoss/owl/commit/b2b0b17c1f436283ee39b7b3b83f7f7fa5b0447f))

## [1.6.0](https://github.com/jwmoss/owl/compare/v1.5.0...v1.6.0) (2026-11-13)


### Features

* **engines:** update dependency mrsirg97-rgb/libosmos to v0.7.0 ([#49](https://github.com/jwmoss/owl/issues/49)) ([e55c566](https://github.com/jwmoss/owl/commit/e55c566048bb5223ad54beb14dd814cc70d31058))
* **engines:** update dependency tailscale/tailscale to v1.104.7 ([#48](https://github.com/jwmoss/owl/issues/48)) ([e82d57b](https://github.com/jwmoss/owl/commit/e82d57bcd4ba8cfa5aa58a000c69ece73b9af801))
* **engines:** update https://huggingface.co/unsloth/qwen3.8-flash-next-gguf digest to f5d175d ([#47](https://github.com/jwmoss/owl/issues/47)) ([8cdebb4](https://github.com/jwmoss/owl/commit/8cdebb4ec8f306c2016ebaeae4895b4e3e1a5b53))

## [1.5.0](https://github.com/jwmoss/owl/compare/v1.4.0...v1.5.0) (2026-11-12)


### Features

* **engines:** update dependency mrsirg97-rgb/libosmos to v0.6.7 ([#41](https://github.com/jwmoss/owl/issues/41)) ([0a5dc3a](https://github.com/jwmoss/owl/commit/0a5dc3a1e55af38f062adc964ea25746f93671ca))
* **engines:** update dependency mw00/project-maya to v1.1.61 ([#42](https://github.com/jwmoss/owl/issues/42)) ([dae4936](https://github.com/jwmoss/owl/commit/dae49369c9ce5e998026a694cd4cb2bb8d076a43))
* **engines:** update ghcr.io/gufo-org/toolboxes/gufo-runtime docker tag to v0.34.0 ([#44](https://github.com/jwmoss/owl/issues/44)) ([0a1b849](https://github.com/jwmoss/owl/commit/0a1b84962bfe7b31583acc1b79cf74fc705d4963))
* **engines:** update ghcr.io/peonist-ai/halogen-flash-server docker tag to v0.20.4 ([#43](https://github.com/jwmoss/owl/issues/43)) ([493ac61](https://github.com/jwmoss/owl/commit/493ac616fd902f2a0e4fea1255909b5c6b5fb7d4))
* **engines:** update https://huggingface.co/peonist-ai/halogen-qwen3.8-flash-next digest to f5a151c ([#40](https://github.com/jwmoss/owl/issues/40)) ([5d0d98a](https://github.com/jwmoss/owl/commit/5d0d98a53c3318e8964672f8b04cb23b0d4effef))

## [1.4.0](https://github.com/jwmoss/owl/compare/v1.3.0...v1.4.0) (2026-11-11)


### Features

* add an optional Tailscale playbook ([#37](https://github.com/jwmoss/owl/issues/37)) ([ab2b41e](https://github.com/jwmoss/owl/commit/ab2b41e2cb47003ae764d98383b982f8bb66553a))

## [1.3.0](https://github.com/jwmoss/owl/compare/v1.2.0...v1.3.0) (2026-11-11)


### Features

* **engines:** update Maya and test Halogen NPU models ([#35](https://github.com/jwmoss/owl/issues/35)) ([7353192](https://github.com/jwmoss/owl/commit/735319294268b40c216bb7e1aa74b9ce25143c11))

## [1.2.0](https://github.com/jwmoss/owl/compare/v1.1.3...v1.2.0) (2026-11-11)


### Features

* **engines:** serve halogen NPU models and pass extra engine env ([#33](https://github.com/jwmoss/owl/issues/33)) ([ba300ae](https://github.com/jwmoss/owl/commit/ba300ae492e468157738d3f16f918d5f264d8652))

## [1.1.3](https://github.com/jwmoss/owl/compare/v1.1.2...v1.1.3) (2026-11-11)


### Bug Fixes

* restore the default engine after failed Strata updates ([#31](https://github.com/jwmoss/owl/issues/31)) ([22ce10f](https://github.com/jwmoss/owl/commit/22ce10fbf38a123b4d91d1439e58d33c03050dc4))

## [1.1.2](https://github.com/jwmoss/owl/compare/v1.1.1...v1.1.2) (2026-11-11)


### Bug Fixes

* update installed Strata components from the pinned feed ([#29](https://github.com/jwmoss/owl/issues/29)) ([176e7fb](https://github.com/jwmoss/owl/commit/176e7fbd64b749311c85992665bc262299ecec05))

## [1.1.1](https://github.com/jwmoss/owl/compare/v1.1.0...v1.1.1) (2026-11-11)


### Bug Fixes

* reserve Maya GPU memory and harden live engine tests ([#27](https://github.com/jwmoss/owl/issues/27)) ([238b6d5](https://github.com/jwmoss/owl/commit/238b6d5739bae961b45feb00013cab26c7734f80))

## [1.1.0](https://github.com/jwmoss/owl/compare/v1.0.0...v1.1.0) (2026-11-11)


### Features

* **engines:** update dependency mrsirg97-rgb/libosmos to v0.6.1 ([fcc35fa](https://github.com/jwmoss/owl/commit/fcc35fa60fcd356016401701f275c0b32f44ad66))
* **engines:** update dependency mw00/project-maya to v1.1.58 ([b3758f4](https://github.com/jwmoss/owl/commit/b3758f4c20e9931a3c0be9a3e3111439372f68f1))
* **engines:** update dependency niko1221/strata to v0.2.13 ([d640750](https://github.com/jwmoss/owl/commit/d6407506ad828a05bbe95947ea96f23335d5ead7))
* **engines:** update ghcr.io/gufo-org/toolboxes/gufo-runtime docker tag to v0.33.0 ([0b4f952](https://github.com/jwmoss/owl/commit/0b4f9529f9b964ad97fa37c84d25878e4e9c2770))
* **engines:** update https://huggingface.co/peonist-ai/halogen-qwen3.8-flash-next digest to 4d104c3 ([fe450b1](https://github.com/jwmoss/owl/commit/fe450b1fb2cf35bf595c2aa3550d2c907619a8a6))
* **engines:** update https://huggingface.co/unsloth/qwen3.8-flash-next-gguf digest to 084c631 ([3fbc8c4](https://github.com/jwmoss/owl/commit/3fbc8c4e557649bd46c396f92762a77e9dfd5040))

## 1.0.0 (2026-11-11)


### Features

* add AGENTS.md and a setup skill for coding agents ([8e27b9b](https://github.com/jwmoss/owl/commit/8e27b9bfde0d15cd90102b304fd6d134a90aacb0))
* **ansible:** add halogen playbook ([6cebf36](https://github.com/jwmoss/owl/commit/6cebf36b83e80b4d7a673013bee8241b13778594))
* **ansible:** add playbooks for Ubuntu, Strata, gufo and libosmos ([6853fe0](https://github.com/jwmoss/owl/commit/6853fe04c8dcd7e215bb0a1100b778c99420d9c8))
* **ansible:** add Project Maya setup playbook ([ff508fc](https://github.com/jwmoss/owl/commit/ff508fc66e038d42d2f06bbd6ee40cdb53753b56))
* **ansible:** automate the owl AI server setup ([19ad31b](https://github.com/jwmoss/owl/commit/19ad31bfe53bb3ecb084edb0b019002cfcd82f96))
* **ansible:** open engines on the LAN and document clients ([476c461](https://github.com/jwmoss/owl/commit/476c461fab02cc3b1f1fd7250296d4a4fa609832))
* **gufo:** add the abliterated model option and turn off Xet downloads ([e3cb335](https://github.com/jwmoss/owl/commit/e3cb33571ca769773e68b567feffcaa8c7902b77))
* **halogen:** add an optional abliterated checkpoint ([d7e5719](https://github.com/jwmoss/owl/commit/d7e571947f66ab91390fd1c0569358e0da00c5b6))
* **halogen:** update to 0.20.1 and restart engines on unit changes ([14db396](https://github.com/jwmoss/owl/commit/14db396e0105607669ee9ad08bc08ae687782c21))
* let a coding agent set up the machine ([c70e0d6](https://github.com/jwmoss/owl/commit/c70e0d6093063236d651d214bd113493e17e5e8c))
* **maya:** add the maya systemd service ([85eeb8b](https://github.com/jwmoss/owl/commit/85eeb8b13e61bedb3a05d77ae575bf0b49a26af5))


### Bug Fixes

* check memory, test only installed engines, rerun on pin changes ([cafd862](https://github.com/jwmoss/owl/commit/cafd8628f994ed4c3f27e7aafa9f170bbcb560fa))
* download large models with aria2c ([a57c879](https://github.com/jwmoss/owl/commit/a57c879c2ca7a523bec6b7a80779ef2e12eb6764))
* engine switch OOMs, rootless podman at boot; halogen default ([25dbcd8](https://github.com/jwmoss/owl/commit/25dbcd898734d00453d816ea1e32a8f5941f2e91))
* **gufo:** download the model with aria2c and check SHA-256 ([47024b4](https://github.com/jwmoss/owl/commit/47024b4c0c584ef49df519da2d6dc7c95171fa97))
* **halogen:** download the abliterated checkpoint with aria2c ([2f69bab](https://github.com/jwmoss/owl/commit/2f69babac4493bd47ca750cf0d3ce555f58780e5))
* make halogen the default and keep the podman user session ([0042aba](https://github.com/jwmoss/owl/commit/0042abaa1f052f99046ded6078bbf009683ef396))
* make the playbooks safe for a new machine ([e9c193c](https://github.com/jwmoss/owl/commit/e9c193cdc312ca63bfa9b2e0d355d0f2d4e9a166))
* wait for free memory before an engine starts ([65a963c](https://github.com/jwmoss/owl/commit/65a963c300de3569b82568fae48301bd78b5d191))
