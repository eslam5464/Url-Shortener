document.getElementById("shortenedUrl").addEventListener("click", function (event) {
  if (event.shiftKey) {
    event.preventDefault();
    var originalUrl = this.href;

    if (!originalUrl.includes("/preview")) {
      var urlParts = originalUrl.split("/");
      var domain = urlParts[2];
      var path = urlParts.slice(3).join("/");
      var newUrl = "http://" + domain + "/preview/" + path;
      this.href = newUrl;
    }

    window.open(this.href, "_blank");
  }
});
