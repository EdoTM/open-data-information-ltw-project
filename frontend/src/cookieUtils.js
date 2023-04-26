export function getCookie(cookie) {
  return document.cookie
    .split("; ")
    .find((row) => row.startsWith(cookie))
    ?.split("=")[1];
}

export function setCookie(cookie, value) {
  document.cookie = `${cookie}=${value}; path=/`;
}
