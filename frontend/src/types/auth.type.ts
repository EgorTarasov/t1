export namespace Auth {
  export type Authenticated = {
    state: "authenticated";
  };

  export type Anonymous = {
    state: "anonymous";
  };

  export type Loading = {
    state: "loading";
  };

  export type State = Authenticated | Anonymous | Loading;
}
