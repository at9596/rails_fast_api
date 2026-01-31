Rails.application.routes.draw do
  resources :computations
  post "process_image", to: "computations#create"
  root to: "computations#index"
end
