class CreateComputations < ActiveRecord::Migration[8.1]
  def change
    create_table :computations do |t|
      t.timestamps
    end
  end
end
