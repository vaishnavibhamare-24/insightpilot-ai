import clsx from "clsx";
import type { ReactNode } from "react";

interface BadgeProps {
  children: ReactNode;
  variant?: "default" | "success" | "warning" | "danger";
}

export function Badge({
  children,
  variant = "default",
}: BadgeProps) {
  return (
    <span
      className={clsx(
        "inline-flex rounded-full px-2.5 py-1 text-xs font-medium",
        {
          "bg-slate-100 text-slate-700":
            variant === "default",
          "bg-emerald-100 text-emerald-700":
            variant === "success",
          "bg-amber-100 text-amber-700":
            variant === "warning",
          "bg-red-100 text-red-700":
            variant === "danger",
        },
      )}
    >
      {children}
    </span>
  );
}