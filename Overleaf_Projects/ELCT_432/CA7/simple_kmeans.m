function [indices, centroids] = simple_kmeans(data, num_clusters)
    % This function implements a simple version of the k-means clustering algorithm.
    % Input:
    %   - data: A one-dimensional array of data points to cluster.
    %   - num_clusters: The number of clusters to form.
    % Output:
    %   - indices: An array of the same length as `data`, where each element is an
    %     integer representing the cluster index to which the corresponding data point
    %     belongs.
    %   - centroids: A one-dimensional array of the computed centroids of each cluster.

    % Initialize centroids randomly by selecting `num_clusters` number of data points
    % from `data`. The selection is made without replacement. The centroids are
    % transposed to create a column vector.
    centroids = data(randperm(length(data), num_clusters))';
    
    % Initialize previous centroids as a zero vector of the same size as `centroids`.
    % This will be used for convergence checking.
    prev_centroids = zeros(size(centroids));
    
    % Initialize `indices` as a zero vector of the same length as `data`. This will
    % store the index of the centroid closest to each data point.
    indices = zeros(size(data));
    
    % Continue the algorithm until the centroids do not change, i.e., the current
    % centroids are equal to the previous centroids (`isequal` function checks this).
    while ~isequal(centroids, prev_centroids)
        % Assign each data point to the closest centroid.
        for i = 1:length(data)
            % Compute the absolute differences between the current point and each centroid.
            % The `min` function returns the smallest difference and its index,
            % which corresponds to the closest centroid. We use `~` to ignore the
            % actual minimum value since we only care about the index.
            [~, indices(i)] = min(abs(centroids - data(i)));
        end
        
        % Update the previous centroids to the current centroids before recomputation.
        prev_centroids = centroids;
        
        % Recompute the centroids by calculating the mean of the data points assigned
        % to each centroid.
        for k = 1:num_clusters
            % Only calculate the mean for data points assigned to the k-th centroid.
            % The condition `indices == k` creates a logical array where elements
            % with the k-th cluster index are true. `mean` computes the mean of these points.
            centroids(k) = mean(data(indices == k));
        end
    end
end
