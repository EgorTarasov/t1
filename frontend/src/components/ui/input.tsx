import * as React from "react";

import { cn } from "@/utils/cn";
import { Label } from "./label";

export type InputProps = React.InputHTMLAttributes<HTMLInputElement>;

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
          className,
        )}
        ref={ref}
        {...props}
      />
    );
  },
);
Input.displayName = "Input";

const IconInput = React.forwardRef<
  HTMLInputElement,
  InputProps & {
    leftIcon?: React.ReactElement;
    rightIcon?: React.ReactElement;
    containerClassName?: string;
    label?: string;
  }
>(
  (
    { leftIcon, rightIcon, className, containerClassName, label, ...props },
    ref,
  ) => {
    return (
      <div className={cn("relative", containerClassName)}>
        {label && <Label htmlFor={props.id}>{label}</Label>}
        <Input
          ref={ref}
          className={cn(leftIcon && "pl-10", rightIcon && "pr-10", className)}
          {...props}
        />
        {leftIcon && (
          <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-foreground *:size-4">
            {leftIcon}
          </div>
        )}
        {rightIcon && (
          <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none text-foreground *:size-4">
            {rightIcon}
          </div>
        )}
      </div>
    );
  },
);

export { Input, IconInput };
