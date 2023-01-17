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
