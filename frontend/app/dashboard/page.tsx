"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useMemo, useState } from "react";

import { getApiBaseUrl } from "@/lib/api-base";
import { redirectIfNoToken } from "@/lib/auth";
import { apiFetch } from "@/lib/api";

import { DashboardShell } from "./sections/DashboardShell";

type LoanRow = {
  id: string;
  amount: string | number;
  status: string;
  total_repayment: string | number;
  outstanding_balance: string | number;
  created_at: string;
};

function parseAmount(value: string | number | null | undefined): number {
  if (value === null || value === undefined || value === "") return 0;
  const n = typeof value === "string" ? Number.parseFloat(value) : value;
  return Number.isFinite(n) ? n : 0;
}

function formatCurrency(value: number): string {
  return value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function formatDate(iso: string | null | undefined): string {
  if (!iso) return "—";
  try {
    return new Date(iso).toLocaleDateString(undefined, {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  } catch {
    return "—";
  }
}

function statusBadgeClass(status: string): string {
  switch (status) {
    case "APPROVED":
      return "badge badge-light-success fw-bold";
    case "PENDING":
      return "badge badge-light-warning fw-bold";
    case "DECLINED":
      return "badge badge-light-danger fw-bold";
    case "REVIEW":
      return "badge badge-light-primary fw-bold";
    case "DISBURSED":
      return "badge badge-light-info fw-bold";
    case "REPAID":
      return "badge badge-light-secondary fw-bold";
    default:
      return "badge badge-light-dark fw-bold";
  }
}

function isActiveLoanStatus(status: string): boolean {
  return status !== "DECLINED" && status !== "REPAID";
}

async function readErrorMessage(response: Response): Promise<string> {
  try {
    const body = (await response.json()) as { detail?: unknown };
    const d = body?.detail;
    if (typeof d === "string") return d;
    if (Array.isArray(d) && d.length > 0) return String(d[0]);
  } catch {
    /* ignore */
  }
  return `Request failed (${response.status}).`;
}

export default function DashboardPage() {
  const router = useRouter();
  const [loans, setLoans] = useState<LoanRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (redirectIfNoToken(router)) {
      return;
    }

    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await apiFetch(`${getApiBaseUrl()}/api/loans/`);
        if (response.status === 401 || response.status === 403) {
          router.replace("/login");
          return;
        }
        if (!response.ok) {
          throw new Error(await readErrorMessage(response));
        }
        const data = await response.json();
        const list = Array.isArray(data) ? data : Array.isArray(data?.results) ? data.results : [];
        setLoans(list as LoanRow[]);
      } catch (err) {
        const message =
          err instanceof Error && err.message === "No access token"
            ? "Unauthorized. Please login again."
            : err instanceof Error
              ? err.message
              : "An error occurred while loading dashboard.";
        if (message.toLowerCase().includes("unauthorized")) {
          router.replace("/login");
          return;
        }
        setError(message);
        setLoans([]);
      } finally {
        setLoading(false);
      }
    };

    void load();
  }, [router]);

  const summary = useMemo(() => {
    const totalLoans = loans.length;
    const activeLoans = loans.filter((l) => isActiveLoanStatus(l.status)).length;
    const outstandingBalance = loans
      .filter((l) => isActiveLoanStatus(l.status))
      .reduce((sum, l) => sum + parseAmount(l.outstanding_balance), 0);
    return { totalLoans, activeLoans, outstandingBalance };
  }, [loans]);

  if (loading) {
    return (
      <DashboardShell userLabel="Member" mainTitle="Loan dashboard">
        <p className="text-gray-600 fw-semibold fs-6 mb-0">Loading dashboard...</p>
      </DashboardShell>
    );
  }

  return (
    <DashboardShell userLabel="Member" mainTitle="Loan dashboard">
      {error ? (
        <div className="alert alert-danger d-flex align-items-center mb-10" role="alert">
          <span>{error}</span>
        </div>
      ) : null}

      <div className="row g-5 g-xl-8 mb-5 mb-xl-8">
        <div className="col-md-6 col-xl-4">
          <div className="card card-flush shadow-sm h-md-100">
            <div className="card-body d-flex flex-column justify-content-between py-8 px-9">
              <div className="d-flex flex-stack mb-3">
                <span className="fs-6 fw-semibold text-gray-500 text-uppercase ls-1">Total loans</span>
                <span className="symbol symbol-45px">
                  <span className="symbol-label bg-light-primary text-primary">
                    <i className="bi bi-collection fs-2" />
                  </span>
                </span>
              </div>
              <span className="fs-2hx fw-bolder text-gray-900">{summary.totalLoans}</span>
            </div>
          </div>
        </div>
        <div className="col-md-6 col-xl-4">
          <div className="card card-flush shadow-sm h-md-100">
            <div className="card-body d-flex flex-column justify-content-between py-8 px-9">
              <div className="d-flex flex-stack mb-3">
                <span className="fs-6 fw-semibold text-gray-500 text-uppercase ls-1">Active loans</span>
                <span className="symbol symbol-45px">
                  <span className="symbol-label bg-light-success text-success">
                    <i className="bi bi-graph-up-arrow fs-2" />
                  </span>
                </span>
              </div>
              <span className="fs-2hx fw-bolder text-gray-900">{summary.activeLoans}</span>
            </div>
          </div>
        </div>
        <div className="col-md-12 col-xl-4">
          <div className="card card-flush shadow-sm h-md-100">
            <div className="card-body d-flex flex-column justify-content-between py-8 px-9">
              <div className="d-flex flex-stack mb-3">
                <span className="fs-6 fw-semibold text-gray-500 text-uppercase ls-1">Outstanding balance</span>
                <span className="symbol symbol-45px">
                  <span className="symbol-label bg-light-warning text-warning">
                    <i className="bi bi-wallet2 fs-2" />
                  </span>
                </span>
              </div>
              <span className="fs-2hx fw-bolder text-gray-900">{formatCurrency(summary.outstandingBalance)}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="card card-flush shadow-sm" id="dashboard-loans">
        <div className="card-header align-items-center py-5 gap-2 gap-md-5">
          <div className="card-title">
            <h2 className="fw-bolder fs-3 mb-0">Your loans</h2>
            <span className="text-gray-500 fs-7 fw-semibold d-block mt-1">Overview of amounts, status, and balances</span>
          </div>
        </div>
        <div className="card-body pt-0">
          {!error && loans.length === 0 ? (
            <div className="text-center py-15 py-md-20 px-5">
              <div className="mb-8">
                <span className="symbol symbol-100px">
                  <span className="symbol-label bg-light-secondary text-gray-600">
                    <i className="bi bi-inbox fs-2x" />
                  </span>
                </span>
              </div>
              <p className="text-gray-700 fw-semibold fs-4 mb-8">No loans yet</p>
              <Link href="/loan" className="btn btn-primary fw-bold">
                Apply for Loan
              </Link>
            </div>
          ) : null}
          {!error && loans.length > 0 ? (
            <div className="table-responsive">
              <table className="table table-row-bordered table-row-gray-300 align-middle gs-0 gy-4">
                <thead>
                  <tr className="fw-bold text-gray-800 border-bottom border-gray-200 fs-7 text-uppercase">
                    <th className="min-w-150px">Amount</th>
                    <th className="min-w-120px">Status</th>
                    <th className="min-w-150px">Total repayment</th>
                    <th className="min-w-150px">Outstanding balance</th>
                    <th className="min-w-130px text-end">Created date</th>
                  </tr>
                </thead>
                <tbody>
                  {loans.map((loan) => (
                    <tr key={loan.id}>
                      <td>
                        <span className="text-gray-900 fw-bold d-block fs-6">
                          {formatCurrency(parseAmount(loan.amount))}
                        </span>
                      </td>
                      <td>
                        <span className={statusBadgeClass(loan.status)}>{loan.status}</span>
                      </td>
                      <td>
                        <span className="text-gray-800 fw-semibold fs-6">
                          {formatCurrency(parseAmount(loan.total_repayment))}
                        </span>
                      </td>
                      <td>
                        <span className="text-gray-800 fw-semibold fs-6">
                          {formatCurrency(parseAmount(loan.outstanding_balance))}
                        </span>
                      </td>
                      <td className="text-end">
                        <span className="text-gray-700 fw-semibold fs-7">{formatDate(loan.created_at)}</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : null}
        </div>
      </div>
    </DashboardShell>
  );
}
