export const getToken = () => localStorage.getItem("token");
export const setToken = (token) => localStorage.setItem("token", token);
export const clearToken = () => localStorage.removeItem("token");

export const getUser = () => {
  try {
    return JSON.parse(localStorage.getItem("user"));
  } catch {
    return null;
  }
};
export const setUser = (user) =>
  localStorage.setItem("user", JSON.stringify(user));
export const clearUser = () => localStorage.removeItem("user");

export const logout = () => {
  clearToken();
  clearUser();
};
