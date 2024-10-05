import { FC, useEffect, useState } from "react";

export type FCVM<T> = FC<{ vm: T }>;

export interface DisposableVm {
  dispose(): void;
}

export const useViewModel = <T extends DisposableVm, U extends any[]>(
  _vm: new (...args: U) => T,
  ...args: U
): T => {
  const [vm] = useState(() => new _vm(...args));

  useEffect(() => vm.dispose, []);

  return vm;
};
