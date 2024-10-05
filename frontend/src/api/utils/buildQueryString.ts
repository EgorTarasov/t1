export type Query = Record<string, string | number | boolean | undefined>;

export const buildQueryString = (
  params: Record<string, string | number | boolean | undefined>,
) => {
  const queryString = new URLSearchParams();
  for (const key in params) {
    if (params[key] !== undefined) {
      queryString.append(key, String(params[key]));
    }
  }
  return queryString.toString();
};
