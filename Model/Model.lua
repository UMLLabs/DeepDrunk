require 'nngraph'
require 'nn'
require 'table'

-- Relevant papers
-- Convolutional Neural Networks for Sentence Classification
-- https://arxiv.org/pdf/1408.5882v2


function test_model()
  model = nn.Sequential()

end



function build_model(word_vector_size, filter_sizes, nn_layer_sizes, dropout_rate)
  filter_sizes_length = table.getn(filter_sizes)
  nn_layer_sizes_length = table.getn(nn_layer_sizes)

  filter_table = nn.ParallelTable()


  for filter_size_i=1, filter_sizes_length do
    filter_size = filter_sizes[filter_size_i]

    filter = nn.Sequential()
    filter:add(nn.SpatialConvolution(1, 1, word_vector_size, filter_size))
    filter:add(nn.ReLU())
    filter:add(nn.SpatialMaxPooling(word_vector_size, filter_size))
    filter:add(nn.Reshape(1, filter_size * ))

    filter_table:add(filter)
  end

  filter_outputs = nn.JoinTable(filter_table)


  for nn_layer_size_i=1, nn_layer_sizes_length do
    layer_size = nn_layer_sizes[nn_layer_size_i]

    model:add(nn.Dropout(dropout_rate))
    model:add(nn.Linear(layer_size))
    model:add(nn.ReLU())
  end

  model:add(nn.Linear())
  model:add(nn.SoftMax())

  return model
end

--model = build_model(100, {2,3,4}, {100}, .5)
model = test_model()
