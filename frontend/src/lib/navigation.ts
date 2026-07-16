import {
  Activity,
  BarChart3,
  Bot,
  BrainCircuit,
  GitBranch,
  LineChart,
  ShieldCheck,
  TerminalSquare,
} from "lucide-react";

export const navigationItems = [
  {
    label: "Dashboard",
    href: "/",
    icon: BarChart3,
  },
  {
    label: "AI Copilot",
    href: "/chat",
    icon: Bot,
  },
  {
    label: "SQL Explorer",
    href: "/sql",
    icon: TerminalSquare,
  },
  {
    label: "Churn Prediction",
    href: "/churn",
    icon: BrainCircuit,
  },
  {
    label: "Revenue Forecast",
    href: "/forecast",
    icon: LineChart,
  },
  {
    label: "Data Quality",
    href: "/data-quality",
    icon: ShieldCheck,
  },
  {
    label: "Model Monitoring",
    href: "/monitoring",
    icon: Activity,
  },
  {
    label: "Architecture",
    href: "/architecture",
    icon: GitBranch,
  },
];