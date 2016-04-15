require 'nngraph'
require 'nn'
require 'table'

local build_model(word_vector_size, filter_sizes)
  filter_sizes_length = table.getn(filter_sizes)

  for filter_size_i=1, filter_sizes_length do
    filter_size = filter_sizes[filter_size_i]

    model = nn.Sequential()
    model:add(nn.SpatialConvolution(1, 1, word_vector_size, filter_size))
    model:add(nn.ReLU())
    model:add(nn.SpatialMaxPooling(word_vector_size, filter_size))
    model:add(nn.Reshape())
  end

  model:add(nn.Linear())
  model:add(nn.ReLU())
  model:add(nn.SoftMax())

end
