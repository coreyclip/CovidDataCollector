source venv/bin/activate
echo "$(date +"%D %T") downloading LA CSA Testing Data"
CSA_RESPONSE=$(python download_LA_CSA_testing_table.py)
echo "$(date +"%D %T") downloading LA case death Data"
CASE_DEATH_RESPONSE=$(python download_LA_case_death_table.py)
CSA_DOWNLOAD_STATUS=$(echo $CSA_RESPONSE | grep "Download.*")
CASE_DEATH_DOWNLOAD_STATUS=$(echo $CASE_DEATH_RESPONSE | grep "Download.*")

if [[ "${CSA_DOWNLOAD_STATUS}" == "Download Failed" ]] || [[ "${CASE_DEATH_DOWNLOAD_STATUS}" == "Download Failed" ]]
then 
    echo "CSA_DOWNLOAD_STATUS: ${CSA_DOWNLOAD_STATUS}"
    echo "CASE_DEATH_DOWNLOAD_STATUS: ${CASE_DEATH_DOWNLOAD_STATUS}"
    exit 1
else
    echo "$(date +"%D %T") performing etl transformations and uploading to google sheets"
    git pull
    python transform_upload_to_gsheets.py
    git add .
    git commit -m 'data pull' 
    git push origin master
fi

echo "$(date +"%D %T"), ${CSA_DOWNLOAD_STATUS}, ${CASE_DEATH_DOWNLOAD_STATUS}" >> download_record.csv

