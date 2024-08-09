export const copyToClipboard = (textToCopy) => {
    navigator.clipboard.writeText(textToCopy)
      .then(() => {
        console.log("Copied to clipboard:", textToCopy);
      })
      .catch((error) => {
        console.error("Failed to copy to clipboard:", error);
      });
  };