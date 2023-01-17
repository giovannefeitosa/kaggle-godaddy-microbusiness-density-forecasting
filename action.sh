# source me

function main() {
  local action="$1"

  case "$action" in
    "download")
      local DOWNLOAD_FILE="io/dataset/godaddy-microbusiness-density-forecasting.zip"
      kaggle competitions download -c godaddy-microbusiness-density-forecasting -p io/dataset
      unzip -f "$DOWNLOAD_FILE" -d io/dataset
      rm -f "$DOWNLOAD_FILE"
      ;;
    *)
      echo "Invalid action: $action"
      exit 1
      ;;
  esac
}

main "$@"
