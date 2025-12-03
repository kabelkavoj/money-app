import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'
import { Transaction } from '../api/client'

interface SpendingChartProps {
  transactions: Transaction[]
}

export default function SpendingChart({ transactions }: SpendingChartProps) {
  // Group transactions by category and sum amounts
  const categorySpending = transactions
    .filter((t) => t.type === 'expense')
    .reduce((acc, t) => {
      const categoryName = t.category?.name || 'Uncategorized'
      const amount = Math.abs(t.amount)
      acc[categoryName] = (acc[categoryName] || 0) + amount
      return acc
    }, {} as Record<string, number>)

  const data = Object.entries(categorySpending).map(([name, value]) => ({
    name,
    value: parseFloat(value.toFixed(2)),
  }))

  const COLORS = [
    '#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6',
    '#EC4899', '#06B6D4', '#84CC16', '#F97316', '#6366F1'
  ]

  if (data.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        No spending data available for this period
      </div>
    )
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
          outerRadius={80}
          fill="#8884d8"
          dataKey="value"
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip formatter={(value: number) => `$${value.toFixed(2)}`} />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  )
}

