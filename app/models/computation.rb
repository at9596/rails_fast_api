class Computation < ApplicationRecord
  has_one_attached :image
  has_one_attached :csv_file
end
