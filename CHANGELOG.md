# Changelog

## 1.0.0 (2026-11-11)


### Features

* add AGENTS.md and a setup skill for coding agents ([8e27b9b](https://github.com/jwmoss/owl/commit/8e27b9bfde0d15cd90102b304fd6d134a90aacb0))
* **ansible:** add halogen playbook ([6cebf36](https://github.com/jwmoss/owl/commit/6cebf36b83e80b4d7a673013bee8241b13778594))
* **ansible:** add playbooks for Ubuntu, Strata, gufo and libosmos ([6853fe0](https://github.com/jwmoss/owl/commit/6853fe04c8dcd7e215bb0a1100b778c99420d9c8))
* **ansible:** add Project Maya setup playbook ([ff508fc](https://github.com/jwmoss/owl/commit/ff508fc66e038d42d2f06bbd6ee40cdb53753b56))
* **ansible:** automate the owl AI server setup ([19ad31b](https://github.com/jwmoss/owl/commit/19ad31bfe53bb3ecb084edb0b019002cfcd82f96))
* **ansible:** open engines on the LAN and document clients ([476c461](https://github.com/jwmoss/owl/commit/476c461fab02cc3b1f1fd7250296d4a4fa609832))
* **gufo:** add the abliterated model option and turn off Xet downloads ([e3cb335](https://github.com/jwmoss/owl/commit/e3cb33571ca769773e68b567feffcaa8c7902b77))
* **gufo:** add the abliterated model option and turn off Xet downloads ([65823cc](https://github.com/jwmoss/owl/commit/65823cc73731f22ea1c4644885054c8d741bbee5))
* **halogen:** add an optional abliterated checkpoint ([d7e5719](https://github.com/jwmoss/owl/commit/d7e571947f66ab91390fd1c0569358e0da00c5b6))
* **halogen:** add an optional abliterated checkpoint ([68cea33](https://github.com/jwmoss/owl/commit/68cea33ce93d9d18e88079538baaf5de7caff75b))
* **halogen:** update to 0.20.1 and restart engines on unit changes ([14db396](https://github.com/jwmoss/owl/commit/14db396e0105607669ee9ad08bc08ae687782c21))
* **halogen:** update to 0.20.1 and restart engines on unit changes ([7376692](https://github.com/jwmoss/owl/commit/7376692d307faf4ceb6fed748bcc25f2524d36e5))
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
