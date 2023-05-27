export interface PostData {
  id: number;
  title: string;
  content: string;
  postImage: string;
  authorUsername: string;
  authorProfilePic: string;
  score: number;
  userVote: UserVote;
  starred: boolean;
  timestamp: string;
  hidden: boolean;
  commentCount: number;
}

export interface CommentData {
  id: number;
  content?: string;
  authorUsername: string;
  authorProfilePic: string;
  timestamp: string;
  likes: number;
  liked: boolean;
}

type UserInfoResponse = {
  username: string;
  email: string;
  profilePic: string;
};

type ProfileInfo = {
  bio: string;
  birthday: string;
  cv?: string;
  email: string;
  profile_pic: string;
  username: string;
  posts: PostData[];
  postCount: number;
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
