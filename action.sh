# source me

function main() {
  local action="$1"
  local param1="$2"
  export PROJECT_ROOT="$(pwd)"

  local pyt="python"

  if [ -z "$(which python)" ]; then
    pyt="python3"
  fi

  case "$action" in
    "run")
      # run app
      $pyt src/dashapp.py
      ;;
    "download")
      echo "$PROJECT_ROOT"
      download_kaggle_dataset
      # ---
      # Download io/customdata/cfips_coordinates.csv
      local CFIPS_COORDINATES_FILE="$PROJECT_ROOT/io/customdata/cfips_coordinates.csv"
      if [ -f "$CFIPS_COORDINATES_FILE" ]; then
        echo "ok. File $CFIPS_COORDINATES_FILE already exists"
      else
        $pyt "$PROJECT_ROOT/etc/python-scripts/download-cfips-coordinates.py"
      fi
      ;;
    *)
      echo "Invalid action: $action"
      ;;
  esac
}

# Download io/dataset
function download_kaggle_dataset() {
  local DOWNLOAD_FILE="$PROJECT_ROOT/io/dataset/godaddy-microbusiness-density-forecasting.zip"
  echo "Downloading io/dataset/*..."
  echo ""
  kaggle competitions download -c godaddy-microbusiness-density-forecasting -p io/dataset
  # unzip file
  if [ -f "$DOWNLOAD_FILE" ]; then
    echo "Extracting file $DOWNLOAD_FILE..."
    unzip -f "$DOWNLOAD_FILE" -d "$PROJECT_ROOT/io/dataset"
  else
    echo ""
    echo "[!] ERROR: File $DOWNLOAD_FILE could not be downloaded"
    echo ""
  fi
  # delete zip file only if the extraction was successful
  if [ -f "$PROJECT_ROOT/io/dataset/train.csv" ]; then
    echo "file $DOWNLOAD_FILE downloaded and extracted"
    rm -f "$DOWNLOAD_FILE"
  else
    echo ""
    echo "[!] ERROR: File $DOWNLOAD_FILE could not be extracted"
  fi
}

main "$@"
