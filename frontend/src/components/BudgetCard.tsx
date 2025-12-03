import { Budget, Transaction } from '../api/client'

interface BudgetStatus {
  budget: Budget
  spent: number
  remaining: number
  percentage: number
  isOverBudget: boolean
}

interface BudgetCardProps {
  status: BudgetStatus
}

export default function BudgetCard({ status }: BudgetCardProps) {
  const { budget, spent, remaining, percentage, isOverBudget } = status

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">
            {budget.category?.name || 'Uncategorized'}
          </h3>
          <p className="text-sm text-gray-500 capitalize">{budget.period}</p>
        </div>
        <div
          className="w-4 h-4 rounded-full"
          style={{ backgroundColor: budget.category?.color || '#3B82F6' }}
        />
      </div>

      <div className="mb-4">
        <div className="flex justify-between text-sm mb-2">
          <span className="text-gray-600">Budgeted</span>
          <span className="font-semibold">${budget.amount.toFixed(2)}</span>
        </div>
        <div className="flex justify-between text-sm mb-2">
          <span className="text-gray-600">Spent</span>
          <span className={`font-semibold ${isOverBudget ? 'text-red-600' : 'text-gray-900'}`}>
            ${spent.toFixed(2)}
          </span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-gray-600">Remaining</span>
          <span className={`font-semibold ${remaining < 0 ? 'text-red-600' : 'text-green-600'}`}>
            ${remaining.toFixed(2)}
          </span>
        </div>
      </div>

      <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
        <div
          className={`h-2 rounded-full transition-all ${
            isOverBudget ? 'bg-red-500' : percentage > 80 ? 'bg-yellow-500' : 'bg-green-500'
          }`}
          style={{ width: `${Math.min(percentage, 100)}%` }}
        />
      </div>
      <p className="text-xs text-gray-500 text-center">
        {percentage.toFixed(1)}% used
      </p>
    </div>
  )
}

