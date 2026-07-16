import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";

export default function LoginPage() {
  const domain =
    process.env.NEXT_PUBLIC_COGNITO_DOMAIN;

  const clientId =
    process.env.NEXT_PUBLIC_COGNITO_CLIENT_ID;

  const redirectUri =
    process.env
      .NEXT_PUBLIC_COGNITO_REDIRECT_URI;

  const loginUrl =
    `${domain}/login?client_id=${clientId}` +
    `&response_type=code` +
    `&scope=openid+email+profile` +
    `&redirect_uri=${encodeURIComponent(
      redirectUri ?? ""
    )}`;

  return (
    <div className="mx-auto max-w-xl space-y-6">
      <section className="text-center">
        <h1 className="text-3xl font-bold text-slate-900">
          Sign in to InsightPilot AI
        </h1>

        <p className="mt-2 text-slate-500">
          Secure authentication powered by Amazon Cognito.
        </p>
      </section>

      <Card>
        <div className="flex justify-center">
          <Badge variant="warning">
            Amazon Cognito
          </Badge>
        </div>

        <h2 className="mt-5 text-center text-xl font-semibold text-slate-900">
          Secure Login
        </h2>

        <p className="mt-3 text-center text-sm leading-6 text-slate-600">
          Click the button below to securely sign in using
          Amazon Cognito.
        </p>

        <div className="mt-6">
          <a
            href={loginUrl}
            className="block w-full rounded-lg bg-blue-600 px-4 py-3 text-center text-sm font-medium text-white hover:bg-blue-700"
          >
            Sign in with Amazon Cognito
          </a>
        </div>
      </Card>
    </div>
  );
}