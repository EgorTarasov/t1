import { toast } from "sonner";
import { z } from "zod";
import { buildQueryString, Query } from "./buildQueryString";
import { authToken } from "./authToken";

const baseUrl = import.meta.env.VITE_API_URL || "https://api.t1.larek.tech";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type Schema = z.ZodType<any, any, any>;
type Path = `/${string}`;

export interface Config<T extends Schema> extends RequestInit {
  schema?: T;
}

const getConfig = <T extends Schema>(config?: Config<T>): Config<T> => ({
  ...config,
  headers: {
    Authorization: `Bearer ${authToken.get()}`,
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "application/json",
    ...(config?.headers ?? {}),
  },
});

const handleError = (error: unknown) => {
  if (error instanceof Error) {
    toast.error("Error", {
      description:
        error.message || "There was an error processing your request",
    });
  } else if (error instanceof z.ZodError) {
    toast.error("Validation error", {
      description: error.errors.map((e) => e.message).join(", "),
    });
  } else {
    toast.error("Error", {
      description: "There was an error processing your request",
    });
  }
  console.error(error);
  throw error;
};

const handleRequest = async <T extends Schema>(
  req: (config?: Config<T>) => Promise<Response>,
  config?: Config<T>,
): Promise<z.infer<T>> => {
  try {
    const res = await req(getConfig(config));

    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }

    const data = (await res.json()) as z.infer<T>;

    return config?.schema ? config.schema.parse(data) : data;
  } catch (e) {
    handleError(e);
  }
};

const get = <T extends Schema>(
  path: Path,
  config?: Config<T> & { search?: Query },
): Promise<z.infer<T>> => {
  const queryString = config?.search
    ? `?${buildQueryString(config.search)}`
    : "";
  return handleRequest(
    (c) => fetch(`${baseUrl}${path}${queryString}`, { ...c, method: "GET" }),
    config,
  );
};

const post = <T extends Schema>(
  path: Path,
  variables?: unknown,
  config?: Config<T>,
): Promise<z.infer<T>> =>
  handleRequest(
    (c) =>
      fetch(`${baseUrl}${path}`, {
        ...c,
        method: "POST",
        body: JSON.stringify(variables),
      }),
    config,
  );

const put = <T extends Schema>(
  path: Path,
  variables?: unknown,
  config?: Config<T>,
): Promise<z.infer<T>> =>
  handleRequest(
    (c) =>
      fetch(`${baseUrl}${path}`, {
        ...c,
        method: "PUT",
        body: JSON.stringify(variables),
      }),
    config,
  );

const del = <T extends Schema>(
  path: Path,
  config?: Config<T>,
): Promise<z.infer<T>> =>
  handleRequest(
    (c) => fetch(`${baseUrl}${path}`, { ...c, method: "DELETE" }),
    config,
  );

export default {
  get,
  post,
  put,
  delete: del,
};
