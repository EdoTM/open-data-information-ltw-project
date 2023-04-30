import md5 from "crypto-js/md5";
import axiosInstance from "./axiosInstance";
import { decodeCredential } from "vue3-google-login";
import { AxiosResponse } from "axios";
import {breakpointsBootstrapV5, useBreakpoints} from "@vueuse/core";

export function generatePasswordMD5(plainPassword: string) {
  return md5(plainPassword).toString();
}

export function sendSignUpRequest(
  signup: SignUpRequest
): Promise<AxiosResponse<SignInResponse>> {
  return axiosInstance.post("/signup", signup);
}

export function sendLoginRequest(
  login: LoginRequest
): Promise<AxiosResponse<SignInResponse>> {
  return axiosInstance.post("/login", login);
}

export function sendGoogleSignInRequest(response: { credential: string }) {
  const userData = decodeCredential(response.credential) as GoogleUserData;
  const { email, id, name } = userData;
  const password = generatePasswordMD5(id);
  const signup: SignUpRequest = {
    email,
    password,
    username: name.replace(" ", "-"),
    birthdate: "2000-01-01",
  };

  return _sendGoogleSignUpRequest(signup);
}

function _sendGoogleSignUpRequest(signup: SignUpRequest) {
  return sendSignUpRequest(signup).catch((error) => {
    const { status, data } = error.response;
    if (status === 409 && data.error.includes("Username")) {
      const login: LoginRequest = {
        email: signup.email,
        password: signup.password,
      };
      return sendLoginRequest(login);
    }
    throw error;
  });
}

export const bs5Breakpoints = useBreakpoints(breakpointsBootstrapV5);