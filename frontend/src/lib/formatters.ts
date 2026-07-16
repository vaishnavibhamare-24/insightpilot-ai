export function formatCurrency(
  value: string | number | null | undefined,
): string {
  const numericValue = Number(value ?? 0);

  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 2,
  }).format(numericValue);
}

export function formatNumber(
  value: string | number | null | undefined,
): string {
  return new Intl.NumberFormat("en-US").format(
    Number(value ?? 0),
  );
}

export function formatPercentage(
  value: string | number | null | undefined,
  digits = 1,
): string {
  return `${Number(value ?? 0).toFixed(digits)}%`;
}

export function formatMilliseconds(
  value: number | null | undefined,
): string {
  return `${Number(value ?? 0).toFixed(0)} ms`;
}