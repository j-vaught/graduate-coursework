%% Clear and close everything
clear; close all; clc;

%% 0. Start by entering your last name
lastName = "Vaught";
disp("EMCH-792 Final Project, " + lastName)

[dataDir, projectRoot] = locateProjectPaths();
reportFigureDir = fullfile(projectRoot, "report", "figures");
reportGeneratedDir = fullfile(projectRoot, "report", "generated");

if ~exist(reportFigureDir, "dir")
    mkdir(reportFigureDir);
end
if ~exist(reportGeneratedDir, "dir")
    mkdir(reportGeneratedDir);
end

palette = brandPalette();

%% Problem I. Load datasets and estimate calibration variances
fpStruct = load(fullfile(dataDir, "FP_data.mat"));
FP_data = fpStruct.FP_data;

y1Calib = load(fullfile(dataDir, "y1_calib_data.mat")).y1_calib_data(:);
y2Calib = load(fullfile(dataDir, "y2_calib_data.mat")).y2_calib_data(:);

time = FP_data.time(:);
dt = mean(diff(time));
if max(abs(diff(time) - dt)) > 1e-10
    error("The deployment dataset does not use a constant sample time.");
end

truth = [FP_data.x(:).'; FP_data.y(:).'; FP_data.psi(:).'; FP_data.u(:).'];
measurements = [FP_data.y1(:).'; FP_data.y2(:).'];
controls = [FP_data.df(:).'; FP_data.a(:).'];

params = struct();
params.dt = dt;
params.lf = 1.0;
params.lr = 1.0;
params.Q = diag([0.01, 0.01, 0.1, 0.05]);
params.processNoiseScale = dt;
params.processNoiseDescription = "sample-period-scaled Q used as the discrete process contribution";
params.R1 = var(y1Calib, 0);
params.R2 = var(y2Calib, 0);
params.x0 = zeros(4, 1);
params.baseP0 = diag([4.0, 4.0, (20 * pi / 180)^2, 0.25]);
params.ukf = struct("alpha", 1e-3, "beta", 2.0, "kappa", 0.0);
params.priorDescription = "zero-centered neutral prior that does not use deployment truth";

data = struct();
data.time = time;
data.truth = truth;
data.measurements = measurements;
data.controls = controls;

%% Problem II through VI. Use the nominal prior, scaled Q, and a fixed scalar gate
params.P0 = params.baseP0;
params.gateThreshold = 6.634896601021214;
params.gateLabel = "99%";
params.gateConfidence = 0.99;

%% Problem II through V. Run the requested filter configurations
configs = [ ...
    buildConfig("ekf_rect_no_gate", "EKF rect., no gate", "ekf", "euler", false, inf), ...
    buildConfig("ukf_rect_no_gate", "UKF rect., no gate", "ukf", "euler", false, inf), ...
    buildConfig("ekf_rect_gate", "EKF rect., gate", "ekf", "euler", true, params.gateThreshold), ...
    buildConfig("ukf_rect_gate", "UKF rect., gate", "ukf", "euler", true, params.gateThreshold), ...
    buildConfig("ukf_rk4_no_gate", "UKF RK4, no gate", "ukf", "rk4", false, inf), ...
    buildConfig("ukf_rk4_gate", "UKF RK4, gate", "ukf", "rk4", true, params.gateThreshold)];

results = struct();
for idx = 1:numel(configs)
    config = configs(idx);
    results.(config.id) = runFilter(data, params, config);
end

appendix = runAblationStudies(data, params);

runtimeProblem3Configs = [configs(1), configs(2)];
runtimeProblem3Stats = measureRuntimes(data, params, runtimeProblem3Configs, 60);

runtimeProblem6Configs = [configs(2), configs(5)];
runtimeProblem6Stats = measureRuntimes(data, params, runtimeProblem6Configs, 60);

%% Problem IV and V. Export report-ready plots and tables
exportTrajectoryFigure(data, results, palette, reportFigureDir);
exportStateFigure(data, results, palette, reportFigureDir);
exportCovarianceFigure(data, results, palette, reportFigureDir);
exportGatingFigure(data, results, params, palette, reportFigureDir);
exportAblationFigures(appendix, palette, reportFigureDir);

summaryPath = fullfile(reportGeneratedDir, "summary.txt");
typstPath = fullfile(reportGeneratedDir, "results.typ");

writeSummaryText(summaryPath, data, params, configs, results, runtimeProblem3Stats, runtimeProblem6Stats, appendix);
writeTypstResults(typstPath, data, params, configs, results, runtimeProblem3Stats, runtimeProblem6Stats, appendix);

%% Problem VI. Print concise conclusions for the report
printConsoleSummary(data, params, configs, results, runtimeProblem3Stats, runtimeProblem6Stats, summaryPath, typstPath);

%% Any functions you develop need to go under here
function [dataDir, projectRoot] = locateProjectPaths()
    candidates = {pwd, fullfile(pwd, "ws")};
    scriptPath = which("Final_project.m");
    if ~isempty(scriptPath)
        candidates{end + 1} = fileparts(scriptPath); %#ok<AGROW>
    end

    dataDir = "";
    for idx = 1:numel(candidates)
        candidate = string(candidates{idx});
        if isfolder(candidate) && isfile(fullfile(candidate, "FP_data.mat"))
            dataDir = candidate;
            break
        end
    end

    if strlength(dataDir) == 0
        error("Unable to locate FP_data.mat. Run the script from the project root or the ws directory.");
    end

    [~, folderName] = fileparts(dataDir);
    if strcmp(string(folderName), "ws")
        projectRoot = fileparts(dataDir);
    else
        projectRoot = dataDir;
    end
end

function config = buildConfig(id, label, filterType, integrator, gating, gateThreshold)
    config = struct( ...
        "id", char(id), ...
        "label", char(label), ...
        "filterType", char(filterType), ...
        "integrator", char(integrator), ...
        "gating", logical(gating), ...
        "gateThreshold", gateThreshold, ...
        "sensorMask", [true; true]);
end

function result = runFilter(data, params, config)
    stateCount = size(data.truth, 1);
    sampleCount = numel(data.time);

    x = params.x0;
    P = params.P0;
    x(3) = wrapAngle(x(3));
    P = stabilizeCovariance(P);

    xHistory = zeros(stateCount, sampleCount);
    pDiagHistory = zeros(stateCount, sampleCount);
    traceHistory = zeros(1, sampleCount);
    accepted = true(2, sampleCount);
    nisHistory = nan(2, sampleCount);
    innovationHistory = nan(2, sampleCount);
    predictionHistory = nan(2, sampleCount);

    xHistory(:, 1) = x;
    pDiagHistory(:, 1) = diag(P);
    traceHistory(1) = trace(P);

    for k = 2:sampleCount
        control = data.controls(:, k - 1);

        if strcmp(config.filterType, "ekf")
            [x, P] = ekfPredict(x, P, control, params);
        else
            [x, P] = ukfPredict(x, P, control, params, config.integrator);
        end

        if config.sensorMask(1)
            [x, P, update1] = scalarMeasurementUpdate(x, P, data.measurements(1, k), 1, params, config);
        else
            update1 = skippedMeasurementUpdate(x, data.measurements(1, k), 1);
        end

        if config.sensorMask(2)
            [x, P, update2] = scalarMeasurementUpdate(x, P, data.measurements(2, k), 2, params, config);
        else
            update2 = skippedMeasurementUpdate(x, data.measurements(2, k), 2);
        end

        accepted(:, k) = [update1.accepted; update2.accepted];
        nisHistory(:, k) = [update1.nis; update2.nis];
        innovationHistory(:, k) = [update1.innovation; update2.innovation];
        predictionHistory(:, k) = [update1.prediction; update2.prediction];

        xHistory(:, k) = x;
        pDiagHistory(:, k) = diag(P);
        traceHistory(k) = trace(P);
    end

    metrics = computeMetrics(xHistory, data.truth, traceHistory, pDiagHistory(:, end));

    result = struct();
    result.id = config.id;
    result.label = config.label;
    result.filterType = config.filterType;
    result.integrator = config.integrator;
    result.gating = config.gating;
    result.x = xHistory;
    result.Pdiag = pDiagHistory;
    result.traceP = traceHistory;
    result.accepted = accepted;
    result.nis = nisHistory;
    result.innovation = innovationHistory;
    result.predictedMeasurement = predictionHistory;
    result.metrics = metrics;
    result.rejections = [sum(~accepted(1, :)), sum(~accepted(2, :))];
    result.finalP = P;
end

function [xPred, PPred] = ekfPredict(x, P, control, params)
    F = bicycleJacobian(x, control, params);
    xPred = propagateEuler(x, control, params);
    Phi = eye(size(P)) + params.dt * F;
    PPred = Phi * P * Phi.' + processNoiseContribution(params);
    xPred(3) = wrapAngle(xPred(3));
    PPred = stabilizeCovariance(PPred);
end

function [xPred, PPred] = ukfPredict(x, P, control, params, integrator)
    [sigmaPoints, Wm, Wc] = unscentedSigmaPoints(x, P, params.ukf);
    propagated = zeros(size(sigmaPoints));

    for idx = 1:size(sigmaPoints, 2)
        propagated(:, idx) = propagateState(sigmaPoints(:, idx), control, params, integrator);
    end

    xPred = weightedStateMean(propagated, Wm);
    PPred = zeros(size(P));

    for idx = 1:size(propagated, 2)
        deviation = propagated(:, idx) - xPred;
        deviation(3) = wrapAngle(deviation(3));
        PPred = PPred + Wc(idx) * (deviation * deviation.');
    end

    PPred = stabilizeCovariance(PPred + processNoiseContribution(params));
end

function [xNext, PNext, update] = scalarMeasurementUpdate(x, P, measurement, sensorId, params, config)
    if strcmp(config.filterType, "ekf")
        [xNext, PNext, update] = ekfScalarUpdate(x, P, measurement, sensorId, params, config);
    else
        [xNext, PNext, update] = ukfScalarUpdate(x, P, measurement, sensorId, params, config);
    end
end

function update = skippedMeasurementUpdate(x, measurement, sensorId)
    prediction = scalarMeasurementValue(x, sensorId);
    update = struct( ...
        "accepted", true, ...
        "nis", nan, ...
        "innovation", measurement - prediction, ...
        "prediction", prediction);
end

function [xNext, PNext, update] = ekfScalarUpdate(x, P, measurement, sensorId, params, config)
    [prediction, H] = scalarMeasurementModel(x, sensorId);
    variance = sensorVariance(sensorId, params);
    innovation = measurement - prediction;
    S = H * P * H.' + variance;
    S = max(S, 1e-12);
    nis = innovation^2 / S;

    update = struct("accepted", true, "nis", nis, "innovation", innovation, "prediction", prediction);

    if config.gating && nis > config.gateThreshold
        xNext = x;
        PNext = P;
        update.accepted = false;
        return
    end

    K = (P * H.') / S;
    xNext = x + K * innovation;
    xNext(3) = wrapAngle(xNext(3));

    identity = eye(size(P));
    PNext = (identity - K * H) * P * (identity - K * H).' + K * variance * K.';
    PNext = stabilizeCovariance(PNext);
end

function [xNext, PNext, update] = ukfScalarUpdate(x, P, measurement, sensorId, params, config)
    [sigmaPoints, Wm, Wc] = unscentedSigmaPoints(x, P, params.ukf);
    sigmaMeasurements = zeros(1, size(sigmaPoints, 2));

    for idx = 1:size(sigmaPoints, 2)
        sigmaMeasurements(idx) = scalarMeasurementValue(sigmaPoints(:, idx), sensorId);
    end

    prediction = sum(Wm .* sigmaMeasurements);
    variance = sensorVariance(sensorId, params);
    S = variance;
    Pxz = zeros(numel(x), 1);

    for idx = 1:size(sigmaPoints, 2)
        stateDeviation = sigmaPoints(:, idx) - x;
        stateDeviation(3) = wrapAngle(stateDeviation(3));
        measurementDeviation = sigmaMeasurements(idx) - prediction;
        S = S + Wc(idx) * measurementDeviation^2;
        Pxz = Pxz + Wc(idx) * stateDeviation * measurementDeviation;
    end

    S = max(S, 1e-12);
    innovation = measurement - prediction;
    nis = innovation^2 / S;

    update = struct("accepted", true, "nis", nis, "innovation", innovation, "prediction", prediction);

    if config.gating && nis > config.gateThreshold
        xNext = x;
        PNext = P;
        update.accepted = false;
        return
    end

    K = Pxz / S;
    xNext = x + K * innovation;
    xNext(3) = wrapAngle(xNext(3));
    PNext = stabilizeCovariance(P - K * S * K.');
end

function [sigmaPoints, Wm, Wc] = unscentedSigmaPoints(x, P, ukfParams)
    n = numel(x);
    lambda = ukfParams.alpha^2 * (n + ukfParams.kappa) - n;
    scaling = n + lambda;
    scaledCovariance = stabilizeCovariance(scaling * P);

    [lower, flag] = chol(scaledCovariance, "lower");
    jitter = 1e-9;
    while flag ~= 0 && jitter <= 1e-3
        scaledCovariance = stabilizeCovariance(scaledCovariance + jitter * eye(n));
        [lower, flag] = chol(scaledCovariance, "lower");
        jitter = 10 * jitter;
    end
    if flag ~= 0
        error("Unable to compute UKF sigma points from the covariance matrix.");
    end

    sigmaPoints = zeros(n, 2 * n + 1);
    sigmaPoints(:, 1) = x;
    for idx = 1:n
        sigmaPoints(:, idx + 1) = x + lower(:, idx);
        sigmaPoints(:, n + idx + 1) = x - lower(:, idx);
    end
    sigmaPoints(3, :) = wrapAngle(sigmaPoints(3, :));

    Wm = [lambda / scaling, repmat(1 / (2 * scaling), 1, 2 * n)];
    Wc = Wm;
    Wc(1) = Wc(1) + (1 - ukfParams.alpha^2 + ukfParams.beta);
end

function meanState = weightedStateMean(points, weights)
    meanState = zeros(size(points, 1), 1);
    meanState([1, 2, 4]) = points([1, 2, 4], :) * weights.';
    meanState(3) = atan2(sum(weights .* sin(points(3, :))), sum(weights .* cos(points(3, :))));
    meanState(3) = wrapAngle(meanState(3));
end

function f = bicycleDynamics(x, control, params)
    steering = control(1);
    acceleration = control(2);
    beta = atan((params.lr / (params.lf + params.lr)) * tan(steering));
    speed = x(4);
    heading = x(3) + beta;

    f = zeros(4, 1);
    f(1) = speed * cos(heading);
    f(2) = speed * sin(heading);
    f(3) = (speed / params.lr) * sin(beta);
    f(4) = acceleration;
end

function F = bicycleJacobian(x, control, params)
    steering = control(1);
    beta = atan((params.lr / (params.lf + params.lr)) * tan(steering));
    speed = x(4);
    heading = x(3) + beta;

    F = zeros(4, 4);
    F(1, 3) = -speed * sin(heading);
    F(1, 4) = cos(heading);
    F(2, 3) = speed * cos(heading);
    F(2, 4) = sin(heading);
    F(3, 4) = sin(beta) / params.lr;
end

function Q = processNoiseContribution(params)
    Q = params.processNoiseScale * params.Q;
end

function xNext = propagateState(x, control, params, integrator)
    switch integrator
        case 'euler'
            xNext = propagateEuler(x, control, params);
        case 'rk4'
            xNext = propagateRK4(x, control, params);
        otherwise
            error("Unknown integrator: %s", integrator);
    end
end

function xNext = propagateEuler(x, control, params)
    xNext = x + params.dt * bicycleDynamics(x, control, params);
    xNext(3) = wrapAngle(xNext(3));
end

function xNext = propagateRK4(x, control, params)
    k1 = bicycleDynamics(x, control, params);
    k2 = bicycleDynamics(wrapState(x + 0.5 * params.dt * k1), control, params);
    k3 = bicycleDynamics(wrapState(x + 0.5 * params.dt * k2), control, params);
    k4 = bicycleDynamics(wrapState(x + params.dt * k3), control, params);

    xNext = x + (params.dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4);
    xNext(3) = wrapAngle(xNext(3));
end

function wrapped = wrapState(x)
    wrapped = x;
    wrapped(3) = wrapAngle(wrapped(3));
end

function angle = wrapAngle(angle)
    angle = atan2(sin(angle), cos(angle));
end

function [prediction, H] = scalarMeasurementModel(x, sensorId)
    switch sensorId
        case 1
            prediction = hypot(x(1), x(2));
            if prediction > 1e-12
                H = [x(1) / prediction, x(2) / prediction, 0, 0];
            else
                H = [0, 0, 0, 0];
            end
        case 2
            prediction = x(3)^3;
            H = [0, 0, 3 * x(3)^2, 0];
        otherwise
            error("Unknown sensor index.");
    end
end

function prediction = scalarMeasurementValue(x, sensorId)
    prediction = scalarMeasurementModel(x, sensorId);
end

function variance = sensorVariance(sensorId, params)
    if sensorId == 1
        variance = params.R1;
    else
        variance = params.R2;
    end
end

function metrics = computeMetrics(estimate, truth, traceHistory, finalPDiag)
    errorHistory = estimate - truth;
    errorHistory(3, :) = wrapAngle(errorHistory(3, :));

    rmse = sqrt(mean(errorHistory.^2, 2));

    metrics = struct();
    metrics.rmse = rmse;
    metrics.positionRMSE = sqrt(mean(errorHistory(1, :).^2 + errorHistory(2, :).^2));
    metrics.headingRMSE = rmse(3);
    metrics.headingRMSEDeg = rad2deg(rmse(3));
    metrics.avgTraceP = mean(traceHistory);
    metrics.finalTraceP = traceHistory(end);
    metrics.finalPDiag = finalPDiag(:);
end

function P = stabilizeCovariance(P)
    P = 0.5 * (P + P.');
    [vectors, values] = eig(P);
    diagonal = real(diag(values));
    diagonal(diagonal < 1e-9) = 1e-9;
    P = vectors * diag(diagonal) * vectors.';
    P = 0.5 * (P + P.');
end

function runtimeStats = measureRuntimes(data, params, configs, repetitions)
    runtimeStats = repmat(struct("label", "", "samples", [], "meanSeconds", 0.0, "stdSeconds", 0.0), numel(configs), 1);

    for idx = 1:numel(configs)
        runFilter(data, params, configs(idx)); %#ok<NASGU>
        samples = zeros(repetitions, 1);
        for rep = 1:repetitions
            startTime = tic;
            runFilter(data, params, configs(idx)); %#ok<NASGU>
            samples(rep) = toc(startTime);
        end

        runtimeStats(idx).label = configs(idx).label;
        runtimeStats(idx).samples = samples;
        runtimeStats(idx).meanSeconds = mean(samples);
        runtimeStats(idx).stdSeconds = std(samples);
    end
end

function appendix = runAblationStudies(data, params)
    appendix = struct();
    appendix.qInterpretation = runQInterpretationComparison(data, params);
    appendix.gating = runGateThresholdAblation(data, params);
    appendix.measurement = runMeasurementAblation(data, params);
    appendix.prior = runPriorScaleAblation(data, params);
    appendix.ukfSpread = runUkfSpreadAblation(data, params);
end

function study = runQInterpretationComparison(data, params)
    labels = ["Direct Q", "Q times dt"];
    scales = [1.0, params.dt];
    descriptions = ["direct discrete Q from the assignment", "sample-period-scaled Q sensitivity check"];
    filters = ["EKF", "UKF"];
    rows = emptyAblationRows();

    for scaleIdx = 1:numel(scales)
        paramsVariant = params;
        paramsVariant.processNoiseScale = scales(scaleIdx);
        paramsVariant.processNoiseDescription = descriptions(scaleIdx);

        for filterIdx = 1:numel(filters)
            config = buildConfig( ...
                "q_interpretation", ...
                sprintf("%s %s", filters(filterIdx), labels(scaleIdx)), ...
                lower(filters(filterIdx)), ...
                "euler", ...
                false, ...
                inf);
            result = runFilter(data, paramsVariant, config);
            rows(end + 1) = ablationRow(filters(filterIdx), labels(scaleIdx), scales(scaleIdx), result); %#ok<AGROW>
        end
    end

    study = struct();
    study.labels = labels;
    study.scales = scales;
    study.rows = rows;
    study.bestPosition = bestAblationRow(rows, "positionRMSE");
    study.bestHeading = bestAblationRow(rows, "headingRMSEDeg");
end

function study = runGateThresholdAblation(data, params)
    gateLabels = ["No gate", "95%", "97.5%", "99%", "99.5%", "99.9%"];
    gateConfidences = [nan, 0.95, 0.975, 0.99, 0.995, 0.999];
    filters = ["EKF", "UKF"];
    rows = emptyAblationRows();

    for filterIdx = 1:numel(filters)
        filterName = lower(filters(filterIdx));
        for gateIdx = 1:numel(gateLabels)
            if isnan(gateConfidences(gateIdx))
                gating = false;
                threshold = inf;
            else
                gating = true;
                threshold = scalarChiSquareThreshold(gateConfidences(gateIdx));
            end

            config = buildConfig( ...
                "gate_sweep", ...
                sprintf("%s %s", filters(filterIdx), gateLabels(gateIdx)), ...
                filterName, ...
                "euler", ...
                gating, ...
                threshold);
            result = runFilter(data, params, config);
            rows(end + 1) = ablationRow(filters(filterIdx), gateLabels(gateIdx), threshold, result); %#ok<AGROW>
        end
    end

    study = struct();
    study.labels = gateLabels;
    study.filters = filters;
    study.rows = rows;
    study.bestPosition = bestAblationRow(rows, "positionRMSE");
    study.bestHeading = bestAblationRow(rows, "headingRMSEDeg");
end

function study = runMeasurementAblation(data, params)
    modeLabels = ["Both sensors", "y1 only", "y2 only", "Prediction only"];
    sensorMasks = {[true; true], [true; false], [false; true], [false; false]};
    filters = ["EKF", "UKF"];
    rows = emptyAblationRows();

    for filterIdx = 1:numel(filters)
        filterName = lower(filters(filterIdx));
        for modeIdx = 1:numel(modeLabels)
            config = buildConfig( ...
                "measurement_sweep", ...
                sprintf("%s %s", filters(filterIdx), modeLabels(modeIdx)), ...
                filterName, ...
                "euler", ...
                false, ...
                inf);
            config.sensorMask = sensorMasks{modeIdx};
            result = runFilter(data, params, config);
            rows(end + 1) = ablationRow(filters(filterIdx), modeLabels(modeIdx), modeIdx, result); %#ok<AGROW>
        end
    end

    study = struct();
    study.labels = modeLabels;
    study.filters = filters;
    study.rows = rows;
    study.bestPosition = bestAblationRow(rows, "positionRMSE");
    study.bestHeading = bestAblationRow(rows, "headingRMSEDeg");
end

function study = runPriorScaleAblation(data, params)
    scales = [0.25, 0.5, 1, 2, 5, 10];
    filters = ["EKF", "UKF"];
    rows = emptyAblationRows();

    for filterIdx = 1:numel(filters)
        filterName = lower(filters(filterIdx));
        for scaleIdx = 1:numel(scales)
            paramsVariant = params;
            paramsVariant.P0 = params.baseP0 * scales(scaleIdx);
            config = buildConfig( ...
                "prior_sweep", ...
                sprintf("%s P0 scale %.2g", filters(filterIdx), scales(scaleIdx)), ...
                filterName, ...
                "euler", ...
                false, ...
                inf);
            result = runFilter(data, paramsVariant, config);
            rows(end + 1) = ablationRow(filters(filterIdx), sprintf("%.2g", scales(scaleIdx)), scales(scaleIdx), result); %#ok<AGROW>
        end
    end

    study = struct();
    study.scales = scales;
    study.filters = filters;
    study.rows = rows;
    study.bestPosition = bestAblationRow(rows, "positionRMSE");
    study.bestHeading = bestAblationRow(rows, "headingRMSEDeg");
end

function study = runUkfSpreadAblation(data, params)
    alphas = [1e-3, 0.03, 0.1, 0.3, 0.7, 1.0];
    rows = emptyAblationRows();

    for alphaIdx = 1:numel(alphas)
        paramsVariant = params;
        paramsVariant.ukf.alpha = alphas(alphaIdx);
        config = buildConfig( ...
            "ukf_spread_sweep", ...
            sprintf("UKF alpha %.3g", alphas(alphaIdx)), ...
            "ukf", ...
            "euler", ...
            false, ...
            inf);
        result = runFilter(data, paramsVariant, config);
        rows(end + 1) = ablationRow("UKF", sprintf("%.3g", alphas(alphaIdx)), alphas(alphaIdx), result); %#ok<AGROW>
    end

    study = struct();
    study.alphas = alphas;
    study.rows = rows;
    study.bestPosition = bestAblationRow(rows, "positionRMSE");
    study.bestHeading = bestAblationRow(rows, "headingRMSEDeg");
end

function threshold = scalarChiSquareThreshold(confidence)
    threshold = 2 * erfinv(confidence)^2;
end

function rows = emptyAblationRows()
    template = struct( ...
        "filter", "", ...
        "setting", "", ...
        "settingValue", 0.0, ...
        "positionRMSE", 0.0, ...
        "headingRMSEDeg", 0.0, ...
        "speedRMSE", 0.0, ...
        "avgTraceP", 0.0, ...
        "rejY1", 0, ...
        "rejY2", 0);
    rows = repmat(template, 0, 1);
end

function row = ablationRow(filterName, settingLabel, settingValue, result)
    row = struct( ...
        "filter", char(filterName), ...
        "setting", char(settingLabel), ...
        "settingValue", settingValue, ...
        "positionRMSE", result.metrics.positionRMSE, ...
        "headingRMSEDeg", result.metrics.headingRMSEDeg, ...
        "speedRMSE", result.metrics.rmse(4), ...
        "avgTraceP", result.metrics.avgTraceP, ...
        "rejY1", result.rejections(1), ...
        "rejY2", result.rejections(2));
end

function row = bestAblationRow(rows, metricName)
    values = zeros(numel(rows), 1);
    for idx = 1:numel(rows)
        values(idx) = rows(idx).(metricName);
    end
    [~, bestIdx] = min(values);
    row = rows(bestIdx);
end

function exportAblationFigures(appendix, palette, outputDir)
    exportGateThresholdAblationFigure(appendix.gating, palette, outputDir);
    exportMeasurementAblationFigure(appendix.measurement, palette, outputDir);
    exportPriorScaleAblationFigure(appendix.prior, palette, outputDir);
    exportUkfSpreadAblationFigure(appendix.ukfSpread, palette, outputDir);
end

function exportGateThresholdAblationFigure(study, palette, outputDir)
    labels = study.labels;
    filters = study.filters;
    xValues = 1:numel(labels);
    colors = {palette.rose, palette.atlantic};

    fig = figure("Visible", "off", "Color", palette.white, "Position", [100, 100, 1050, 720]);
    tiled = tiledlayout(fig, 2, 1, "TileSpacing", "compact", "Padding", "compact");
    metrics = {"positionRMSE", "headingRMSEDeg"};
    yLabels = {"Position RMSE (m)", "Heading RMSE (deg)"};

    for metricIdx = 1:numel(metrics)
        ax = nexttile(tiled);
        hold(ax, "on");
        for filterIdx = 1:numel(filters)
            values = ablationSeries(study.rows, filters(filterIdx), labels, metrics{metricIdx});
            plot(ax, xValues, values, "-o", "Color", colors{filterIdx}, "LineWidth", 1.8, ...
                "MarkerSize", 5.5, "DisplayName", filters(filterIdx));
        end
        xlim(ax, [0.75, numel(labels) + 0.25]);
        set(ax, "XTick", xValues, "XTickLabel", cellstr(labels));
        ylabel(ax, yLabels{metricIdx});
        styleAxes(ax, palette);
        if metricIdx == 1
            title(ax, "Scalar Gate Threshold Sweep");
            lgd = legend(ax, "Location", "northoutside", "Orientation", "horizontal");
            lgd.Layout.Tile = "north";
        else
            xlabel(ax, "Gate confidence");
        end
    end

    exportgraphics(fig, fullfile(outputDir, "ablation_gate_thresholds.png"), "Resolution", 300);
    close(fig);
end

function exportMeasurementAblationFigure(study, palette, outputDir)
    labels = study.labels;
    filters = study.filters;
    colors = [palette.rose; palette.atlantic];

    fig = figure("Visible", "off", "Color", palette.white, "Position", [100, 100, 1050, 720]);
    tiled = tiledlayout(fig, 2, 1, "TileSpacing", "compact", "Padding", "compact");
    metrics = {"positionRMSE", "headingRMSEDeg"};
    yLabels = {"Position RMSE (m)", "Heading RMSE (deg)"};

    for metricIdx = 1:numel(metrics)
        ax = nexttile(tiled);
        values = zeros(numel(labels), numel(filters));
        for filterIdx = 1:numel(filters)
            values(:, filterIdx) = ablationSeries(study.rows, filters(filterIdx), labels, metrics{metricIdx});
        end
        bars = bar(ax, values, "grouped");
        for barIdx = 1:numel(bars)
            bars(barIdx).FaceColor = colors(barIdx, :);
            bars(barIdx).EdgeColor = palette.black;
            bars(barIdx).LineWidth = 0.75;
        end
        set(ax, "XTickLabel", cellstr(labels));
        ylabel(ax, yLabels{metricIdx});
        styleAxes(ax, palette);
        if metricIdx == 1
            title(ax, "Sensor Contribution Ablation");
            lgd = legend(ax, cellstr(filters), "Location", "northoutside", "Orientation", "horizontal");
            lgd.Layout.Tile = "north";
        else
            xlabel(ax, "Measurements used");
        end
    end

    exportgraphics(fig, fullfile(outputDir, "ablation_measurements.png"), "Resolution", 300);
    close(fig);
end

function exportPriorScaleAblationFigure(study, palette, outputDir)
    scales = study.scales;
    filters = study.filters;
    colors = {palette.rose, palette.atlantic};

    fig = figure("Visible", "off", "Color", palette.white, "Position", [100, 100, 1050, 720]);
    tiled = tiledlayout(fig, 2, 1, "TileSpacing", "compact", "Padding", "compact");
    metrics = {"positionRMSE", "headingRMSEDeg"};
    yLabels = {"Position RMSE (m)", "Heading RMSE (deg)"};

    for metricIdx = 1:numel(metrics)
        ax = nexttile(tiled);
        hold(ax, "on");
        for filterIdx = 1:numel(filters)
            values = ablationNumericSeries(study.rows, filters(filterIdx), scales, metrics{metricIdx});
            semilogx(ax, scales, values, "-o", "Color", colors{filterIdx}, "LineWidth", 1.8, ...
                "MarkerSize", 5.5, "DisplayName", filters(filterIdx));
        end
        set(ax, "XTick", scales, "XTickLabel", compose("%.2g", scales));
        ylabel(ax, yLabels{metricIdx});
        styleAxes(ax, palette);
        if metricIdx == 1
            title(ax, "Initial Covariance Scale Sweep");
            lgd = legend(ax, "Location", "northoutside", "Orientation", "horizontal");
            lgd.Layout.Tile = "north";
        else
            xlabel(ax, "Multiplier on nominal P_0");
        end
    end

    exportgraphics(fig, fullfile(outputDir, "ablation_prior_scale.png"), "Resolution", 300);
    close(fig);
end

function exportUkfSpreadAblationFigure(study, palette, outputDir)
    alphas = study.alphas;

    fig = figure("Visible", "off", "Color", palette.white, "Position", [100, 100, 1050, 720]);
    tiled = tiledlayout(fig, 2, 1, "TileSpacing", "compact", "Padding", "compact");
    metrics = {"positionRMSE", "headingRMSEDeg"};
    yLabels = {"Position RMSE (m)", "Heading RMSE (deg)"};
    colors = {palette.atlantic, palette.horseshoe};

    for metricIdx = 1:numel(metrics)
        ax = nexttile(tiled);
        values = ablationNumericSeries(study.rows, "UKF", alphas, metrics{metricIdx});
        semilogx(ax, alphas, values, "-o", "Color", colors{metricIdx}, "LineWidth", 1.8, "MarkerSize", 5.5);
        set(ax, "XTick", alphas, "XTickLabel", compose("%.3g", alphas));
        ylabel(ax, yLabels{metricIdx});
        styleAxes(ax, palette);
        if metricIdx == 1
            title(ax, "UKF Sigma-Point Spread Sweep");
        else
            xlabel(ax, "UKF alpha");
        end
    end

    exportgraphics(fig, fullfile(outputDir, "ablation_ukf_spread.png"), "Resolution", 300);
    close(fig);
end

function values = ablationSeries(rows, filterName, settings, metricName)
    values = zeros(numel(settings), 1);
    for settingIdx = 1:numel(settings)
        values(settingIdx) = ablationMetricBySetting(rows, filterName, settings(settingIdx), metricName);
    end
end

function values = ablationNumericSeries(rows, filterName, settings, metricName)
    values = zeros(numel(settings), 1);
    for settingIdx = 1:numel(settings)
        values(settingIdx) = ablationMetricByValue(rows, filterName, settings(settingIdx), metricName);
    end
end

function value = ablationMetricBySetting(rows, filterName, settingLabel, metricName)
    value = nan;
    for idx = 1:numel(rows)
        sameFilter = strcmp(rows(idx).filter, char(filterName));
        sameSetting = strcmp(rows(idx).setting, char(settingLabel));
        if sameFilter && sameSetting
            value = rows(idx).(metricName);
            return
        end
    end
end

function value = ablationMetricByValue(rows, filterName, settingValue, metricName)
    value = nan;
    for idx = 1:numel(rows)
        sameFilter = strcmp(rows(idx).filter, char(filterName));
        sameSetting = abs(rows(idx).settingValue - settingValue) < 1e-12;
        if sameFilter && sameSetting
            value = rows(idx).(metricName);
            return
        end
    end
end

function exportTrajectoryFigure(data, results, palette, outputDir)
    fig = figure("Visible", "off", "Color", palette.white, "Position", [100, 100, 900, 450]);
    ax = axes(fig);
    hold(ax, "on");

    plot(ax, data.truth(1, :), data.truth(2, :), "Color", palette.black, "LineWidth", 2.2, "DisplayName", "Truth");
    plot(ax, results.ekf_rect_no_gate.x(1, :), results.ekf_rect_no_gate.x(2, :), "--", "Color", palette.gray70, "LineWidth", 1.5, "DisplayName", results.ekf_rect_no_gate.label);
    plot(ax, results.ukf_rect_no_gate.x(1, :), results.ukf_rect_no_gate.x(2, :), "--", "Color", palette.atlantic, "LineWidth", 1.5, "DisplayName", results.ukf_rect_no_gate.label);
    plot(ax, results.ekf_rect_gate.x(1, :), results.ekf_rect_gate.x(2, :), "-", "Color", palette.rose, "LineWidth", 1.8, "DisplayName", results.ekf_rect_gate.label);
    plot(ax, results.ukf_rect_gate.x(1, :), results.ukf_rect_gate.x(2, :), "-", "Color", palette.garnet, "LineWidth", 2.0, "DisplayName", results.ukf_rect_gate.label);
    plot(ax, results.ukf_rk4_no_gate.x(1, :), results.ukf_rk4_no_gate.x(2, :), "-", "Color", palette.horseshoe, "LineWidth", 2.0, "DisplayName", results.ukf_rk4_no_gate.label);

    xlabel(ax, "x (m)");
    ylabel(ax, "y (m)");
    title(ax, "Trajectory Comparison");
    axis(ax, "equal");
    styleAxes(ax, palette);
    lgd = legend(ax, "Location", "northeast");
    lgd.Box = "on";
    lgd.Color = palette.white;
    lgd.EdgeColor = palette.black;
    exportgraphics(fig, fullfile(outputDir, "trajectory.png"), "Resolution", 300);
    close(fig);
end

function exportStateFigure(data, results, palette, outputDir)
    fig = figure("Visible", "off", "Color", palette.white, "Position", [100, 100, 1100, 900]);
    tiled = tiledlayout(fig, 4, 1, "TileSpacing", "compact", "Padding", "compact");
    stateNames = {"x (m)", "y (m)", "\psi (deg)", "u (m/s)"};

    comparison = { ...
        struct("matrix", data.truth, "color", palette.black, "style", "-", "width", 2.0, "label", "Truth"), ...
        struct("matrix", results.ekf_rect_no_gate.x, "color", palette.gray70, "style", "--", "width", 1.5, "label", results.ekf_rect_no_gate.label), ...
        struct("matrix", results.ukf_rect_no_gate.x, "color", palette.atlantic, "style", "--", "width", 1.6, "label", results.ukf_rect_no_gate.label), ...
        struct("matrix", results.ukf_rk4_no_gate.x, "color", palette.horseshoe, "style", "-", "width", 1.8, "label", results.ukf_rk4_no_gate.label)};

    for stateIdx = 1:4
        ax = nexttile(tiled);
        hold(ax, "on");

        for seriesIdx = 1:numel(comparison)
            series = comparison{seriesIdx};
            values = series.matrix(stateIdx, :);
            if stateIdx == 3
                values = rad2deg(values);
            end
            plot(ax, data.time, values, "LineStyle", series.style, "Color", series.color, "LineWidth", series.width, "DisplayName", series.label);
        end

        ylabel(ax, stateNames{stateIdx});
        styleAxes(ax, palette);
        if stateIdx == 1
            title(ax, "State Estimates Versus Time");
            lgd = legend(ax, "Location", "northoutside", "Orientation", "horizontal");
            lgd.Layout.Tile = "north";
        end
        if stateIdx == 4
            xlabel(ax, "Time (s)");
        end
    end

    exportgraphics(fig, fullfile(outputDir, "state_timeseries.png"), "Resolution", 300);
    close(fig);
end

function exportCovarianceFigure(data, results, palette, outputDir)
    fig = figure("Visible", "off", "Color", palette.white, "Position", [100, 100, 1100, 900]);
    tiled = tiledlayout(fig, 4, 1, "TileSpacing", "compact", "Padding", "compact");
    labels = {"P_{11}", "P_{22}", "P_{33}", "P_{44}"};

    for idx = 1:4
        ax = nexttile(tiled);
        hold(ax, "on");
        plot(ax, data.time, results.ekf_rect_no_gate.Pdiag(idx, :), "Color", palette.gray70, "LineWidth", 1.6, "DisplayName", results.ekf_rect_no_gate.label);
        plot(ax, data.time, results.ukf_rect_no_gate.Pdiag(idx, :), "Color", palette.atlantic, "LineWidth", 1.8, "DisplayName", results.ukf_rect_no_gate.label);
        plot(ax, data.time, results.ukf_rk4_no_gate.Pdiag(idx, :), "Color", palette.horseshoe, "LineWidth", 1.8, "DisplayName", results.ukf_rk4_no_gate.label);
        ylabel(ax, labels{idx});
        styleAxes(ax, palette);
        if idx == 1
            title(ax, "Diagonal Covariance History");
            lgd = legend(ax, "Location", "northoutside", "Orientation", "horizontal");
            lgd.Layout.Tile = "north";
        end
        if idx == 4
            xlabel(ax, "Time (s)");
        end
    end

    exportgraphics(fig, fullfile(outputDir, "covariance.png"), "Resolution", 300);
    close(fig);
end

function exportGatingFigure(data, results, params, palette, outputDir)
    fig = figure("Visible", "off", "Color", palette.white, "Position", [100, 100, 1100, 700]);
    tiled = tiledlayout(fig, 2, 1, "TileSpacing", "compact", "Padding", "compact");

    sensorNames = {"Sensor y_1 NIS", "Sensor y_2 NIS"};
    for sensorIdx = 1:2
        ax = nexttile(tiled);
        hold(ax, "on");
        plot(ax, data.time, results.ekf_rect_gate.nis(sensorIdx, :), "Color", palette.rose, "LineWidth", 1.5, "DisplayName", results.ekf_rect_gate.label);
        plot(ax, data.time, results.ukf_rect_gate.nis(sensorIdx, :), "Color", palette.garnet, "LineWidth", 1.8, "DisplayName", results.ukf_rect_gate.label);
        yline(ax, params.gateThreshold, "--", "Color", palette.black, "LineWidth", 1.3, "DisplayName", sprintf("Gate = %.2f", params.gateThreshold));

        ekfRejected = ~results.ekf_rect_gate.accepted(sensorIdx, :);
        scatter(ax, data.time(ekfRejected), results.ekf_rect_gate.nis(sensorIdx, ekfRejected), 28, "s", ...
            "MarkerEdgeColor", palette.rose, "MarkerFaceColor", palette.white, "LineWidth", 1.0, "DisplayName", "EKF rejected");

        ukfRejected = ~results.ukf_rect_gate.accepted(sensorIdx, :);
        scatter(ax, data.time(ukfRejected), results.ukf_rect_gate.nis(sensorIdx, ukfRejected), 36, "x", ...
            "MarkerEdgeColor", palette.horseshoe, "LineWidth", 1.2, "DisplayName", "UKF rejected");

        ylabel(ax, sensorNames{sensorIdx});
        styleAxes(ax, palette);
        if sensorIdx == 1
            title(ax, "Normalized Innovation Squared Diagnostics");
            lgd = legend(ax, "Location", "northoutside", "Orientation", "horizontal");
            lgd.Layout.Tile = "north";
        end
        if sensorIdx == 2
            xlabel(ax, "Time (s)");
        end
    end

    exportgraphics(fig, fullfile(outputDir, "gating_diagnostics.png"), "Resolution", 300);
    close(fig);
end

function styleAxes(ax, palette)
    set(ax, ...
        "FontName", "Helvetica", ...
        "FontSize", 11, ...
        "LineWidth", 1.0, ...
        "Box", "on", ...
        "XColor", palette.black, ...
        "YColor", palette.black, ...
        "GridColor", palette.gray50, ...
        "GridAlpha", 0.22, ...
        "MinorGridColor", palette.gray30, ...
        "MinorGridAlpha", 0.16, ...
        "Layer", "top");
    grid(ax, "on");
end

function palette = brandPalette()
    palette = struct();
    palette.garnet = [115, 0, 10] / 255;
    palette.black = [0, 0, 0] / 255;
    palette.white = [255, 255, 255] / 255;
    palette.gray90 = [54, 54, 54] / 255;
    palette.gray70 = [92, 92, 92] / 255;
    palette.gray50 = [162, 162, 162] / 255;
    palette.gray30 = [199, 199, 199] / 255;
    palette.gray10 = [235, 235, 235] / 255;
    palette.warmGrey = [103, 97, 86] / 255;
    palette.sandstorm = [255, 242, 227] / 255;
    palette.rose = [204, 46, 64] / 255;
    palette.atlantic = [70, 106, 159] / 255;
    palette.congaree = [31, 65, 77] / 255;
    palette.horseshoe = [101, 120, 11] / 255;
    palette.grass = [206, 211, 24] / 255;
    palette.honeycomb = [164, 145, 55] / 255;
end

function writeSummaryText(filePath, data, params, configs, results, runtimeProblem3Stats, runtimeProblem6Stats, appendix)
    fid = fopen(filePath, "w");
    if fid < 0
        error("Unable to open summary output file.");
    end
    cleaner = onCleanup(@() fclose(fid));

    fprintf(fid, "EMCH-792 Final Project Summary\n");
    fprintf(fid, "Generated: %s\n\n", char(datetime("now", "Format", "yyyy-MM-dd HH:mm:ss")));

    fprintf(fid, "Problem I. Calibration variances\n");
    fprintf(fid, "  y1 variance = %.6f\n", params.R1);
    fprintf(fid, "  y2 variance = %.6f\n", params.R2);
    fprintf(fid, "  dt = %.3f s\n\n", params.dt);

    fprintf(fid, "Problem II and IV settings\n");
    fprintf(fid, "  nominal P0 diagonal = [%.4f, %.4f, %.4f, %.4f]\n", diag(params.P0));
    fprintf(fid, "  initial prior = %s\n", params.priorDescription);
    fprintf(fid, "  process noise = %s (scale %.3f)\n", params.processNoiseDescription, params.processNoiseScale);
    fprintf(fid, "  scalar gate = %s (threshold %.4f)\n\n", params.gateLabel, params.gateThreshold);

    fprintf(fid, "Filter comparison\n");
    writeTrimmedLine(fid, "  %-20s %-8s %-8s %-10s %-8s %-10s %-10s %-8s %-8s", ...
        "Configuration", "x", "y", "psi deg", "u", "pos", "avg tr(P)", "rej y1", "rej y2");
    for idx = 1:numel(configs)
        result = results.(configs(idx).id);
        writeTrimmedLine(fid, "  %-20s %-8.4f %-8.4f %-10.4f %-8.4f %-10.4f %-10.4f %-8d %-8d", ...
            result.label, result.metrics.rmse(1), result.metrics.rmse(2), result.metrics.headingRMSEDeg, ...
            result.metrics.rmse(4), result.metrics.positionRMSE, result.metrics.avgTraceP, ...
            result.rejections(1), result.rejections(2));
    end
    fprintf(fid, "\n");

    fprintf(fid, "Problem III. Vanilla EKF and UKF runtime (%d repetitions each)\n", numel(runtimeProblem3Stats(1).samples));
    writeTrimmedLine(fid, "  %-20s %-12s %-12s", "Configuration", "Mean ms", "Std ms");
    for idx = 1:numel(runtimeProblem3Stats)
        writeTrimmedLine(fid, "  %-20s %-12.3f %-12.3f", runtimeProblem3Stats(idx).label, ...
            1000 * runtimeProblem3Stats(idx).meanSeconds, 1000 * runtimeProblem3Stats(idx).stdSeconds);
    end

    fprintf(fid, "\nProblem IV. Gating comparison\n");
    fprintf(fid, "  EKF position RMSE: %.4f -> %.4f m\n", results.ekf_rect_no_gate.metrics.positionRMSE, results.ekf_rect_gate.metrics.positionRMSE);
    fprintf(fid, "  EKF heading RMSE: %.4f -> %.4f deg\n", results.ekf_rect_no_gate.metrics.headingRMSEDeg, results.ekf_rect_gate.metrics.headingRMSEDeg);
    fprintf(fid, "  EKF rejections: y1 = %d, y2 = %d\n", results.ekf_rect_gate.rejections(1), results.ekf_rect_gate.rejections(2));
    fprintf(fid, "  UKF position RMSE: %.4f -> %.4f m\n", results.ukf_rect_no_gate.metrics.positionRMSE, results.ukf_rect_gate.metrics.positionRMSE);
    fprintf(fid, "  UKF heading RMSE: %.4f -> %.4f deg\n", results.ukf_rect_no_gate.metrics.headingRMSEDeg, results.ukf_rect_gate.metrics.headingRMSEDeg);
    fprintf(fid, "  UKF rejections: y1 = %d, y2 = %d\n", results.ukf_rect_gate.rejections(1), results.ukf_rect_gate.rejections(2));

    fprintf(fid, "\nProblem V. UKF integrator comparison\n");
    fprintf(fid, "  Rectangular UKF position RMSE = %.4f m\n", results.ukf_rect_no_gate.metrics.positionRMSE);
    fprintf(fid, "  RK4 UKF position RMSE = %.4f m\n", results.ukf_rk4_no_gate.metrics.positionRMSE);
    fprintf(fid, "  Rectangular UKF heading RMSE = %.4f deg\n", results.ukf_rect_no_gate.metrics.headingRMSEDeg);
    fprintf(fid, "  RK4 UKF heading RMSE = %.4f deg\n", results.ukf_rk4_no_gate.metrics.headingRMSEDeg);

    fprintf(fid, "\nProblem VI. UKF runtime by integrator (%d repetitions each)\n", numel(runtimeProblem6Stats(1).samples));
    writeTrimmedLine(fid, "  %-20s %-12s %-12s", "Configuration", "Mean ms", "Std ms");
    for idx = 1:numel(runtimeProblem6Stats)
        writeTrimmedLine(fid, "  %-20s %-12.3f %-12.3f", runtimeProblem6Stats(idx).label, ...
            1000 * runtimeProblem6Stats(idx).meanSeconds, 1000 * runtimeProblem6Stats(idx).stdSeconds);
    end

    fprintf(fid, "\nAppendix ablation highlights\n");
    fprintf(fid, "  Q interpretation best position: %s, %s, %.4f m\n", ...
        appendix.qInterpretation.bestPosition.filter, appendix.qInterpretation.bestPosition.setting, appendix.qInterpretation.bestPosition.positionRMSE);
    fprintf(fid, "  Gate sweep best position: %s, %s, %.4f m\n", ...
        appendix.gating.bestPosition.filter, appendix.gating.bestPosition.setting, appendix.gating.bestPosition.positionRMSE);
    fprintf(fid, "  Gate sweep best heading: %s, %s, %.4f deg\n", ...
        appendix.gating.bestHeading.filter, appendix.gating.bestHeading.setting, appendix.gating.bestHeading.headingRMSEDeg);
    fprintf(fid, "  Sensor sweep best position: %s, %s, %.4f m\n", ...
        appendix.measurement.bestPosition.filter, appendix.measurement.bestPosition.setting, appendix.measurement.bestPosition.positionRMSE);
    fprintf(fid, "  Prior sweep best position: %s, scale %s, %.4f m\n", ...
        appendix.prior.bestPosition.filter, appendix.prior.bestPosition.setting, appendix.prior.bestPosition.positionRMSE);
    fprintf(fid, "  UKF alpha sweep best position: alpha %s, %.4f m\n", ...
        appendix.ukfSpread.bestPosition.setting, appendix.ukfSpread.bestPosition.positionRMSE);

    %#ok<NASGU>
end

function writeTrimmedLine(fid, formatSpec, varargin)
    fprintf(fid, "%s\n", strip(sprintf(formatSpec, varargin{:}), "right"));
end

function writeTypstResults(filePath, data, params, configs, results, runtimeProblem3Stats, runtimeProblem6Stats, appendix)
    fid = fopen(filePath, "w");
    if fid < 0
        error("Unable to open Typst output file.");
    end
    cleaner = onCleanup(@() fclose(fid));

    bestConfig = configs(1);
    bestPosition = inf;
    for idx = 1:numel(configs)
        candidate = results.(configs(idx).id);
        if candidate.metrics.positionRMSE < bestPosition
            bestPosition = candidate.metrics.positionRMSE;
            bestConfig = configs(idx);
        end
    end

    ekfGatingPositionChange = results.ekf_rect_gate.metrics.positionRMSE - results.ekf_rect_no_gate.metrics.positionRMSE;
    ukfGatingPositionChange = results.ukf_rect_gate.metrics.positionRMSE - results.ukf_rect_no_gate.metrics.positionRMSE;
    ekfGatingHeadingChange = results.ekf_rect_gate.metrics.headingRMSEDeg - results.ekf_rect_no_gate.metrics.headingRMSEDeg;
    ukfGatingHeadingImprovement = results.ukf_rect_no_gate.metrics.headingRMSEDeg - results.ukf_rect_gate.metrics.headingRMSEDeg;
    rk4Improvement = results.ukf_rect_no_gate.metrics.positionRMSE - results.ukf_rk4_no_gate.metrics.positionRMSE;
    rk4RuntimePenalty = runtimeProblem6Stats(2).meanSeconds - runtimeProblem6Stats(1).meanSeconds;

    fprintf(fid, '#let generated_on = "%s"\n', typstString(char(datetime("now", "Format", "yyyy-MM-dd HH:mm:ss"))));
    fprintf(fid, '#let dt_text = "%s"\n', sprintf("%.3f", params.dt));
    fprintf(fid, '#let y1_variance_text = "%s"\n', sprintf("%.6f", params.R1));
    fprintf(fid, '#let y2_variance_text = "%s"\n', sprintf("%.6f", params.R2));
    fprintf(fid, '#let p0_trace_ratio_text = "%s"\n', sprintf("%.2f", trace(params.P0) / trace(params.baseP0)));
    fprintf(fid, '#let process_noise_description_text = "%s"\n', typstString(params.processNoiseDescription));
    fprintf(fid, '#let process_noise_scale_text = "%s"\n', sprintf("%.3f", params.processNoiseScale));
    fprintf(fid, '#let chosen_gate_label = "%s"\n', typstString(params.gateLabel));
    fprintf(fid, '#let chosen_gate_threshold_text = "%s"\n', sprintf("%.4f", params.gateThreshold));
    fprintf(fid, '#let best_configuration_text = "%s"\n', typstString(bestConfig.label));
    fprintf(fid, '#let best_position_rmse_text = "%s"\n', sprintf("%.4f", bestPosition));
    fprintf(fid, '#let ekf_gating_position_change_text = "%s"\n', sprintf("%.4f", ekfGatingPositionChange));
    fprintf(fid, '#let ukf_gating_position_change_text = "%s"\n', sprintf("%.4f", ukfGatingPositionChange));
    fprintf(fid, '#let ekf_gating_heading_change_text = "%s"\n', sprintf("%.4f", ekfGatingHeadingChange));
    fprintf(fid, '#let ukf_gating_heading_improvement_text = "%s"\n', sprintf("%.4f", ukfGatingHeadingImprovement));
    fprintf(fid, '#let rk4_position_improvement_text = "%s"\n', sprintf("%.4f", rk4Improvement));
    fprintf(fid, '#let rk4_runtime_penalty_text = "%s"\n\n', sprintf("%.3f", 1000 * rk4RuntimePenalty));

    for idx = 1:numel(configs)
        configId = configs(idx).id;
        result = results.(configId);
        fprintf(fid, '#let %s_pos_text = "%s"\n', configId, sprintf("%.4f", result.metrics.positionRMSE));
        fprintf(fid, '#let %s_heading_deg_text = "%s"\n', configId, sprintf("%.4f", result.metrics.headingRMSEDeg));
        fprintf(fid, '#let %s_speed_text = "%s"\n', configId, sprintf("%.4f", result.metrics.rmse(4)));
        fprintf(fid, '#let %s_avg_trace_text = "%s"\n', configId, sprintf("%.4f", result.metrics.avgTraceP));
        fprintf(fid, '#let %s_rej_y1_text = "%d"\n', configId, result.rejections(1));
        fprintf(fid, '#let %s_rej_y2_text = "%d"\n', configId, result.rejections(2));
    end
    fprintf(fid, '#let ekf_rect_no_gate_runtime_ms_text = "%s"\n', sprintf("%.3f", 1000 * runtimeProblem3Stats(1).meanSeconds));
    fprintf(fid, '#let ukf_rect_no_gate_runtime_ms_text = "%s"\n', sprintf("%.3f", 1000 * runtimeProblem3Stats(2).meanSeconds));
    fprintf(fid, '#let ukf_rect_runtime_ms_text = "%s"\n', sprintf("%.3f", 1000 * runtimeProblem6Stats(1).meanSeconds));
    fprintf(fid, '#let ukf_rk4_runtime_ms_text = "%s"\n\n', sprintf("%.3f", 1000 * runtimeProblem6Stats(2).meanSeconds));

    fprintf(fid, '#let gate_best_position_filter_text = "%s"\n', typstString(appendix.gating.bestPosition.filter));
    fprintf(fid, '#let gate_best_position_setting_text = "%s"\n', typstString(appendix.gating.bestPosition.setting));
    fprintf(fid, '#let gate_best_position_rmse_text = "%s"\n', sprintf("%.4f", appendix.gating.bestPosition.positionRMSE));
    fprintf(fid, '#let gate_best_heading_filter_text = "%s"\n', typstString(appendix.gating.bestHeading.filter));
    fprintf(fid, '#let gate_best_heading_setting_text = "%s"\n', typstString(appendix.gating.bestHeading.setting));
    fprintf(fid, '#let gate_best_heading_rmse_text = "%s"\n', sprintf("%.4f", appendix.gating.bestHeading.headingRMSEDeg));
    fprintf(fid, '#let measurement_best_position_filter_text = "%s"\n', typstString(appendix.measurement.bestPosition.filter));
    fprintf(fid, '#let measurement_best_position_setting_text = "%s"\n', typstString(appendix.measurement.bestPosition.setting));
    fprintf(fid, '#let measurement_best_position_rmse_text = "%s"\n', sprintf("%.4f", appendix.measurement.bestPosition.positionRMSE));
    fprintf(fid, '#let measurement_best_heading_filter_text = "%s"\n', typstString(appendix.measurement.bestHeading.filter));
    fprintf(fid, '#let measurement_best_heading_setting_text = "%s"\n', typstString(appendix.measurement.bestHeading.setting));
    fprintf(fid, '#let measurement_best_heading_rmse_text = "%s"\n', sprintf("%.4f", appendix.measurement.bestHeading.headingRMSEDeg));
    fprintf(fid, '#let prior_best_position_filter_text = "%s"\n', typstString(appendix.prior.bestPosition.filter));
    fprintf(fid, '#let prior_best_position_scale_text = "%s"\n', typstString(appendix.prior.bestPosition.setting));
    fprintf(fid, '#let prior_best_position_rmse_text = "%s"\n', sprintf("%.4f", appendix.prior.bestPosition.positionRMSE));
    fprintf(fid, '#let ukf_alpha_best_position_text = "%s"\n', typstString(appendix.ukfSpread.bestPosition.setting));
    fprintf(fid, '#let ukf_alpha_best_position_rmse_text = "%s"\n', sprintf("%.4f", appendix.ukfSpread.bestPosition.positionRMSE));
    fprintf(fid, '#let ukf_alpha_best_heading_text = "%s"\n', typstString(appendix.ukfSpread.bestHeading.setting));
    fprintf(fid, '#let ukf_alpha_best_heading_rmse_text = "%s"\n\n', sprintf("%.4f", appendix.ukfSpread.bestHeading.headingRMSEDeg));

    fprintf(fid, '#let q_best_position_filter_text = "%s"\n', typstString(appendix.qInterpretation.bestPosition.filter));
    fprintf(fid, '#let q_best_position_setting_text = "%s"\n', typstString(appendix.qInterpretation.bestPosition.setting));
    fprintf(fid, '#let q_best_position_rmse_text = "%s"\n', sprintf("%.4f", appendix.qInterpretation.bestPosition.positionRMSE));
    fprintf(fid, '#let q_best_heading_filter_text = "%s"\n', typstString(appendix.qInterpretation.bestHeading.filter));
    fprintf(fid, '#let q_best_heading_setting_text = "%s"\n', typstString(appendix.qInterpretation.bestHeading.setting));
    fprintf(fid, '#let q_best_heading_rmse_text = "%s"\n\n', sprintf("%.4f", appendix.qInterpretation.bestHeading.headingRMSEDeg));

    writeTypstTableStart(fid, "metrics_table", "9", "(left, right, right, right, right, right, right, right, right)", "5pt");
    writeTypstTableHeader(fid, "[Configuration], [x], [y], [psi deg], [u], [pos.], [avg tr(P)], [rej y1], [rej y2]");
    for idx = 1:numel(configs)
        result = results.(configs(idx).id);
        fprintf(fid, "  [%s], [%s], [%s], [%s], [%s], [%s], [%s], [%d], [%d],\n", ...
            typstString(result.label), sprintf("%.4f", result.metrics.rmse(1)), sprintf("%.4f", result.metrics.rmse(2)), ...
            sprintf("%.4f", result.metrics.headingRMSEDeg), sprintf("%.4f", result.metrics.rmse(4)), ...
            sprintf("%.4f", result.metrics.positionRMSE), sprintf("%.4f", result.metrics.avgTraceP), ...
            result.rejections(1), result.rejections(2));
    end
    writeTypstTableEnd(fid, 1 + numel(configs));

    writeTypstTableStart(fid, "problem3_runtime_table", "3", "(left, right, right)", "6pt");
    writeTypstTableHeader(fid, "[Configuration], [Mean ms], [Std ms]");
    for idx = 1:numel(runtimeProblem3Stats)
        fprintf(fid, "  [%s], [%s], [%s],\n", ...
            typstString(runtimeProblem3Stats(idx).label), sprintf("%.3f", 1000 * runtimeProblem3Stats(idx).meanSeconds), ...
            sprintf("%.3f", 1000 * runtimeProblem3Stats(idx).stdSeconds));
    end
    writeTypstTableEnd(fid, 1 + numel(runtimeProblem3Stats));

    writeTypstTableStart(fid, "problem6_runtime_table", "3", "(left, right, right)", "6pt");
    writeTypstTableHeader(fid, "[Configuration], [Mean ms], [Std ms]");
    for idx = 1:numel(runtimeProblem6Stats)
        fprintf(fid, "  [%s], [%s], [%s],\n", ...
            typstString(runtimeProblem6Stats(idx).label), sprintf("%.3f", 1000 * runtimeProblem6Stats(idx).meanSeconds), ...
            sprintf("%.3f", 1000 * runtimeProblem6Stats(idx).stdSeconds));
    end
    writeTypstTableEnd(fid, 1 + numel(runtimeProblem6Stats));

    writeTypstTableStart(fid, "q_interpretation_table", "7", "(left, left, right, right, right, right, right)", "4pt");
    writeTypstTableHeader(fid, "[Filter], [Q treatment], [scale], [Pos. RMSE], [Heading deg], [u RMSE], [avg tr(P)]");
    for idx = 1:numel(appendix.qInterpretation.rows)
        row = appendix.qInterpretation.rows(idx);
        fprintf(fid, "  [%s], [%s], [%s], [%s], [%s], [%s], [%s],\n", ...
            typstString(row.filter), typstString(row.setting), sprintf("%.3f", row.settingValue), ...
            sprintf("%.4f", row.positionRMSE), sprintf("%.4f", row.headingRMSEDeg), ...
            sprintf("%.4f", row.speedRMSE), sprintf("%.4f", row.avgTraceP));
    end
    writeTypstTableEnd(fid, 1 + numel(appendix.qInterpretation.rows));

    writeTypstTableStart(fid, "gate_ablation_table", "8", "(left, left, right, right, right, right, right, right)", "4pt");
    writeTypstTableHeader(fid, "[Filter], [Gate], [Threshold], [Pos. RMSE], [Heading deg], [u RMSE], [avg tr(P)], [rej y1/y2]");
    for idx = 1:numel(appendix.gating.rows)
        row = appendix.gating.rows(idx);
        fprintf(fid, "  [%s], [%s], [%s], [%s], [%s], [%s], [%s], [%d/%d],\n", ...
            typstString(row.filter), typstString(row.setting), thresholdText(row.settingValue), ...
            sprintf("%.4f", row.positionRMSE), sprintf("%.4f", row.headingRMSEDeg), ...
            sprintf("%.4f", row.speedRMSE), sprintf("%.4f", row.avgTraceP), row.rejY1, row.rejY2);
    end
    writeTypstTableEnd(fid, 1 + numel(appendix.gating.rows));

    writeTypstTableStart(fid, "measurement_ablation_table", "7", "(left, left, right, right, right, right, right)", "4pt");
    writeTypstTableHeader(fid, "[Filter], [Measurements], [Pos. RMSE], [Heading deg], [u RMSE], [avg tr(P)], [rej y1/y2]");
    for idx = 1:numel(appendix.measurement.rows)
        row = appendix.measurement.rows(idx);
        fprintf(fid, "  [%s], [%s], [%s], [%s], [%s], [%s], [%d/%d],\n", ...
            typstString(row.filter), typstString(row.setting), sprintf("%.4f", row.positionRMSE), ...
            sprintf("%.4f", row.headingRMSEDeg), sprintf("%.4f", row.speedRMSE), ...
            sprintf("%.4f", row.avgTraceP), row.rejY1, row.rejY2);
    end
    writeTypstTableEnd(fid, 1 + numel(appendix.measurement.rows));

    writeTypstTableStart(fid, "prior_ablation_table", "6", "(left, right, right, right, right, right)", "4pt");
    writeTypstTableHeader(fid, "[Filter], [$P_0$ scale], [Pos. RMSE], [Heading deg], [u RMSE], [avg tr(P)]");
    for idx = 1:numel(appendix.prior.rows)
        row = appendix.prior.rows(idx);
        fprintf(fid, "  [%s], [%s], [%s], [%s], [%s], [%s],\n", ...
            typstString(row.filter), typstString(row.setting), sprintf("%.4f", row.positionRMSE), ...
            sprintf("%.4f", row.headingRMSEDeg), sprintf("%.4f", row.speedRMSE), sprintf("%.4f", row.avgTraceP));
    end
    writeTypstTableEnd(fid, 1 + numel(appendix.prior.rows));

    writeTypstTableStart(fid, "ukf_spread_ablation_table", "5", "(right, right, right, right, right)", "5pt");
    writeTypstTableHeader(fid, "[$alpha$], [Pos. RMSE], [Heading deg], [u RMSE], [avg tr(P)]");
    for idx = 1:numel(appendix.ukfSpread.rows)
        row = appendix.ukfSpread.rows(idx);
        fprintf(fid, "  [%s], [%s], [%s], [%s], [%s],\n", ...
            typstString(row.setting), sprintf("%.4f", row.positionRMSE), sprintf("%.4f", row.headingRMSEDeg), ...
            sprintf("%.4f", row.speedRMSE), sprintf("%.4f", row.avgTraceP));
    end
    writeTypstTableEnd(fid, 1 + numel(appendix.ukfSpread.rows));

    fprintf(fid, "#let dataset_note = [The script used %d samples at #dt_text s and initialized the filters from a zero-centered prior with the nominal base covariance so the comparisons did not consume deployment truth as estimator input.]\n", numel(data.time));
end

function textValue = thresholdText(value)
    if isinf(value)
        textValue = "inf";
    else
        textValue = sprintf("%.4f", value);
    end
end

function writeTypstTableStart(fid, name, columnsText, alignText, insetText)
    fprintf(fid, '#let %s = table(\n', name);
    fprintf(fid, '  columns: %s,\n', columnsText);
    fprintf(fid, '  align: %s,\n', alignText);
    fprintf(fid, '  inset: %s,\n', insetText);
    fprintf(fid, '  stroke: none,\n');
    fprintf(fid, '  table.hline(y: 0, stroke: 0.8pt + rgb("#000000")),\n');
end

function writeTypstTableHeader(fid, headerText)
    fprintf(fid, '  table.header(%s),\n', headerText);
    fprintf(fid, '  table.hline(y: 1, stroke: 0.5pt + rgb("#000000")),\n');
end

function writeTypstTableEnd(fid, rowCount)
    fprintf(fid, '  table.hline(y: %d, stroke: 0.8pt + rgb("#000000")),\n', rowCount);
    fprintf(fid, ')\n\n');
end

function escaped = typstString(value)
    escaped = strrep(value, '\', '\\');
    escaped = strrep(escaped, '"', '\"');
end

function printConsoleSummary(data, params, configs, results, runtimeProblem3Stats, runtimeProblem6Stats, summaryPath, typstPath)
    fprintf("\nProblem I\n");
    fprintf("  y1 calibration variance: %.6f\n", params.R1);
    fprintf("  y2 calibration variance: %.6f\n", params.R2);
    fprintf("  sample time: %.3f s (%d samples)\n", params.dt, numel(data.time));

    fprintf("\nSelected Settings\n");
    fprintf("  P0 scale: %.2f\n", trace(params.P0) / trace(params.baseP0));
    fprintf("  process noise: %s (scale %.3f)\n", params.processNoiseDescription, params.processNoiseScale);
    fprintf("  scalar gate: %s (threshold %.4f)\n", params.gateLabel, params.gateThreshold);
    fprintf("  UKF scaling: alpha = %.4g, beta = %.1f, kappa = %.1f\n", params.ukf.alpha, params.ukf.beta, params.ukf.kappa);

    fprintf("\nFilter Comparison\n");
    fprintf("  %-20s %-8s %-8s %-10s %-8s %-10s %-10s %-8s %-8s\n", ...
        "Configuration", "x", "y", "psi deg", "u", "pos", "avg tr(P)", "rej y1", "rej y2");
    for idx = 1:numel(configs)
        result = results.(configs(idx).id);
        fprintf("  %-20s %-8.4f %-8.4f %-10.4f %-8.4f %-10.4f %-10.4f %-8d %-8d\n", ...
            result.label, result.metrics.rmse(1), result.metrics.rmse(2), result.metrics.headingRMSEDeg, ...
            result.metrics.rmse(4), result.metrics.positionRMSE, result.metrics.avgTraceP, ...
            result.rejections(1), result.rejections(2));
    end

    fprintf("\nProblem III Runtime Comparison\n");
    fprintf("  %-20s %-12s %-12s\n", "Configuration", "Mean ms", "Std ms");
    for idx = 1:numel(runtimeProblem3Stats)
        fprintf("  %-20s %-12.3f %-12.3f\n", runtimeProblem3Stats(idx).label, ...
            1000 * runtimeProblem3Stats(idx).meanSeconds, 1000 * runtimeProblem3Stats(idx).stdSeconds);
    end

    fprintf("\nProblem VI Runtime Comparison\n");
    fprintf("  %-20s %-12s %-12s\n", "Configuration", "Mean ms", "Std ms");
    for idx = 1:numel(runtimeProblem6Stats)
        fprintf("  %-20s %-12.3f %-12.3f\n", runtimeProblem6Stats(idx).label, ...
            1000 * runtimeProblem6Stats(idx).meanSeconds, 1000 * runtimeProblem6Stats(idx).stdSeconds);
    end

    fprintf("\nArtifacts\n");
    fprintf("  Summary text: %s\n", summaryPath);
    fprintf("  Typst fragment: %s\n", typstPath);
    fprintf("  Figures: %s\n", fullfile(fileparts(summaryPath), "..", "figures"));
end
