type UserInfoResponse = {
  username: string;
  email: string;
  profilePic: string;
};

type SignUpRequest = {
  username: string;
  password: string;
  email: string;
  birthdate: string;
};

type LoginRequest = {
  email: string;
  password: string;
};

type SignInResponse = {
  status: "success";
  username: string;
  email: string;
};

type GoogleUserData = {
  email: string;
  email_verified: boolean;
  family_name: string;
  given_name: string;
  name: string;
  picture: string;
  sub: string;
};
