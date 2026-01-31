class ComputationsController < ApplicationController
  before_action :set_computation, only: %i[show edit update]

  def index
    @data = PythonApiService.get_status
  end

  def new; end

  def edit; end

  def show; end

  def create
    image_file = params[:image]

    if image_file.present?
      result = PythonApiService.process_image(image_file)

      if result[:success]
        return send_data(
          result[:body],
          filename: "blurred_#{image_file.original_filename}",
          type: result[:content_type]
        )
      else
        flash[:alert] = result[:error]
      end
    else
      flash[:alert] = "Please select an image first."
    end

    render :new
  end

  def update
    uploaded_file = params.dig(:computation, :csv_file)

    if uploaded_file.present?
      @computation.csv_file.attach(uploaded_file)
      result = PythonApiService.analyze_csv(uploaded_file)

      if result[:success]
        @csv_analysis = result[:data]
        flash.now[:notice] = "Analysis Successful"
      else
        flash.now[:alert] = result[:error]
      end
    end

    render :edit
  end

  private

  def set_computation
    @computation = Computation.find(params[:id])
  end
end
