import { useEffect, useState } from 'react'
import { budgetsApi, transactionsApi, Budget, Transaction } from '../api/client'
import { format, startOfMonth, endOfMonth } from 'date-fns'
import BudgetCard from '../components/BudgetCard'
import SpendingChart from '../components/SpendingChart'

export default function Dashboard() {
  const [budgets, setBudgets] = useState<Budget[]>([])
  const [transactions, setTransactions] = useState<Transaction[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      const [budgetsRes, transactionsRes] = await Promise.all([
        budgetsApi.getAll(),
        transactionsApi.getAll({
          start_date: format(startOfMonth(new Date()), 'yyyy-MM-dd'),
          end_date: format(endOfMonth(new Date()), 'yyyy-MM-dd'),
        }),
      ])
      setBudgets(budgetsRes.data)
      setTransactions(transactionsRes.data)
      setError(null)
    } catch (err) {
      setError('Failed to load data. Make sure the backend is running.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  // Calculate spending per budget category
  const budgetStatus = budgets.map((budget) => {
    const categoryTransactions = transactions.filter(
      (t) => t.category_id === budget.category_id && t.type === 'expense'
    )
    const spent = Math.abs(
      categoryTransactions.reduce((sum, t) => sum + t.amount, 0)
    )
    const remaining = budget.amount - spent
    const percentage = (spent / budget.amount) * 100

    return {
      budget,
      spent,
      remaining,
      percentage,
      isOverBudget: spent > budget.amount,
    }
  })

  const totalBudgeted = budgets.reduce((sum, b) => sum + b.amount, 0)
  const totalSpent = Math.abs(
    transactions
      .filter((t) => t.type === 'expense')
      .reduce((sum, t) => sum + t.amount, 0)
  )
  const totalIncome = transactions
    .filter((t) => t.type === 'income')
    .reduce((sum, t) => sum + t.amount, 0)

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-800">{error}</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-gray-900">Financial Overview</h2>
        <p className="mt-1 text-sm text-gray-500">
          {format(new Date(), 'MMMM yyyy')}
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-3">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                  <span className="text-green-600 text-lg">💰</span>
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Total Income
                  </dt>
                  <dd className="text-lg font-semibold text-gray-900">
                    ${totalIncome.toFixed(2)}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                  <span className="text-blue-600 text-lg">📊</span>
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Total Budgeted
                  </dt>
                  <dd className="text-lg font-semibold text-gray-900">
                    ${totalBudgeted.toFixed(2)}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center">
                  <span className="text-red-600 text-lg">💸</span>
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Total Spent
                  </dt>
                  <dd className="text-lg font-semibold text-gray-900">
                    ${totalSpent.toFixed(2)}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Budget Status */}
      <div>
        <h3 className="text-xl font-semibold text-gray-900 mb-4">
          Budget Status
        </h3>
        {budgetStatus.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-8 text-center">
            <p className="text-gray-500">
              No budgets set up yet. Create your first budget to get started!
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {budgetStatus.map((status) => (
              <BudgetCard key={status.budget.id} status={status} />
            ))}
          </div>
        )}
      </div>

      {/* Spending Chart */}
      {transactions.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">
            Spending by Category
          </h3>
          <SpendingChart transactions={transactions} />
        </div>
      )}
    </div>
  )
}

