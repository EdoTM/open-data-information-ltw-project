export function getCookie(cookie: string) {
  return document.cookie
    .split("; ")
    .find((row) => row.startsWith(cookie))
    ?.split("=")[1];
}

export function setCookie(cookie: string, value: string) {
  document.cookie = `${cookie}=${value}; path=/`;
}

export function deleteCookie(cookie: string) {
  setCookie(cookie, "");
}
