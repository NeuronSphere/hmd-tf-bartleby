# run the test suite

robot --pythonpath ./test_suite \
--settag hmd_repo_name:$HMD_REPO_NAME \
--settag hmd_repo_version:$HMD_REPO_VERSION \
--settag hmd_did:$HMD_DID \
--include Transform* \
test_suite

