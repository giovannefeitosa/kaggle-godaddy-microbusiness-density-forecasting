# source me

function main() {
  local action="$1"
  local param1="$2"
  export PROJECT_ROOT="$(pwd)"

  case "$action" in
    "run")
      # run app
      python src/dashapp.py
      ;;
    "download")
      local DOWNLOAD_FILE="io/dataset/godaddy-microbusiness-density-forecasting.zip"
      kaggle competitions download -c godaddy-microbusiness-density-forecasting -p io/dataset
      unzip -f "$DOWNLOAD_FILE" -d io/dataset
      rm -f "$DOWNLOAD_FILE"
      ;;
    *)
      echo "Invalid action: $action"
      ;;
  esac
}

main "$@"
