import { useEffect, useState } from 'react'
import { budgetsApi, categoriesApi, Budget, Category } from '../api/client'
import BudgetForm from '../components/BudgetForm'

export default function Budgets() {
  const [budgets, setBudgets] = useState<Budget[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingBudget, setEditingBudget] = useState<Budget | null>(null)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [budgetsRes, categoriesRes] = await Promise.all([
        budgetsApi.getAll(),
        categoriesApi.getAll(),
      ])
      setBudgets(budgetsRes.data)
      setCategories(categoriesRes.data)
    } catch (err) {
      console.error('Failed to load data:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = () => {
    setEditingBudget(null)
    setShowForm(true)
  }

  const handleEdit = (budget: Budget) => {
    setEditingBudget(budget)
    setShowForm(true)
  }

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this budget?')) return

    try {
      await budgetsApi.delete(id)
      await loadData()
    } catch (err) {
      console.error('Failed to delete budget:', err)
      alert('Failed to delete budget')
    }
  }

  const handleFormClose = () => {
    setShowForm(false)
    setEditingBudget(null)
    loadData()
  }

  if (loading) {
    return <div className="text-center py-8">Loading...</div>
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Budgets</h2>
          <p className="mt-1 text-sm text-gray-500">
            Manage your monthly budgets by category
          </p>
        </div>
        <button
          onClick={handleCreate}
          className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors"
        >
          + New Budget
        </button>
      </div>

      {showForm && (
        <BudgetForm
          budget={editingBudget}
          categories={categories}
          onClose={handleFormClose}
        />
      )}

      {budgets.length === 0 ? (
        <div className="bg-white rounded-lg shadow p-8 text-center">
          <p className="text-gray-500 mb-4">
            No budgets created yet. Create your first budget to get started!
          </p>
          <button
            onClick={handleCreate}
            className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700"
          >
            Create Budget
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {budgets.map((budget) => (
            <div
              key={budget.id}
              className="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow"
            >
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    {budget.category?.name || 'Uncategorized'}
                  </h3>
                  <p className="text-sm text-gray-500 capitalize">
                    {budget.period}
                  </p>
                </div>
                <div
                  className="w-4 h-4 rounded-full"
                  style={{ backgroundColor: budget.category?.color || '#3B82F6' }}
                />
              </div>
              <div className="mb-4">
                <p className="text-2xl font-bold text-gray-900">
                  ${budget.amount.toFixed(2)}
                </p>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => handleEdit(budget)}
                  className="flex-1 text-sm text-primary-600 hover:text-primary-700 font-medium"
                >
                  Edit
                </button>
                <button
                  onClick={() => handleDelete(budget.id)}
                  className="flex-1 text-sm text-red-600 hover:text-red-700 font-medium"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

