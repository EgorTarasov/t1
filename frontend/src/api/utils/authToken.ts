const tokenKey = "authToken";

let token: string | null = null;

const get = (): string | null => {
  if (token) return token;
  return localStorage[tokenKey] ?? null;
};

const set = (newToken: string) => {
  localStorage[tokenKey] = newToken;
  token = newToken;
};

const remove = () => {
  localStorage.removeItem(tokenKey);
  token = null;
};

export const authToken = Object.assign(
  {},
  {
    get,
    set,
    remove,
  },
);
