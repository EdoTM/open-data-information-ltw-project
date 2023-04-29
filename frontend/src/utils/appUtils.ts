import md5 from "crypto-js/md5";
import axiosInstance from "./axiosInstance";

export function generatePasswordMD5(plainPassword: string) {
  return md5(plainPassword).toString();
}

export function sendSignUpRequest(signup: SignUpRequest): Promise<SignInResponse> {
  return axiosInstance.post("/signup", signup);
}

export function sendLoginRequest(login: LoginRequest): Promise<SignInResponse> {
  return axiosInstance.post("/login", login)
}

