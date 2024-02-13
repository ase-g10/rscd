import service from "@/utils/request";

// Function to request redirection to GitHub for authentication
export function loginWithGithub() {
  return service({
    url: "um/auth2/redirect_to_github1",
    method: "get"
  });
}
