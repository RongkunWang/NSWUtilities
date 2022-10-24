# Tune Json
```
cd JsonTuner/configs
```
First copy from the google excel into summary.tsv 

Run `generateFromTSV.py`

Then go to `app` of the repository, run `batch_tuneTriggerJson.py`.

Notice that in this step, please modify `batch_tuneTriggerJson.py` as needed, as it contains source directory and target directory for the json repo. Make sure both are up to date as master.

Then go to the target repository, commit and push the changes, and make a merge request.

