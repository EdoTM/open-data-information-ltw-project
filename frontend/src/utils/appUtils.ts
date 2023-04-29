import md5 from "crypto-js/md5";
import axiosInstance from "./axiosInstance";
import {getInputElementById} from "./tsUtils";

export function generatePasswordMD5(plainPassword: string) {
  return md5(plainPassword).toString();
}

export type SignUpRequest = {
  username: string;
  password: string;
  email: string;
  birthdate: string;
}

export type LoginRequest = {
  email: string
  password: string
};

export type SignInResponse = {
  status: "success"
  username: string
  email: string
}

export function sendSignUpRequest(signup: SignUpRequest): Promise<SignInResponse> {
  return axiosInstance.post("/signup", signup);
}

export function sendLoginRequest(login: LoginRequest): Promise<SignInResponse> {
  return axiosInstance.post("/login", login)
}

