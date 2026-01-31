require "test_helper"

class ComputationsControllerTest < ActionDispatch::IntegrationTest
  test "should get index" do
    get computations_index_url
    assert_response :success
  end
end
