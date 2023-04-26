import md5 from "crypto-js/md5";

export function generatePasswordMD5(plainPassword: string) {
  return md5(plainPassword).toString();
}