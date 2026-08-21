function record_mechanics_explorer_videos(mode)
%RECORD_MECHANICS_EXPLORER_VIDEOS Record the native 3D model playback.

arguments
    mode (1, 1) string {mustBeMember(mode, ...
        ["all", "preview", "capture_full", "capture_slow"])} = "all"
end

project_directory = fileparts(mfilename("fullpath"));
original_directory = pwd;
cleanup_directory = onCleanup(@() cd(original_directory));
cd(project_directory);

files = output_files();
switch mode
    case "all"
        run_capture_process(project_directory, "capture_full", files.full_frames);
        encode_frame_stream(files.full_frames, files.full_video, 30);
        run_capture_process(project_directory, "capture_slow", files.slow_frames);
        encode_frame_stream(files.slow_frames, files.slow_video, 30);
        save_still_frames(files.full_video);
        delete_if_present(files.full_raw);
        delete_if_present(files.full_frames);
        delete_if_present(files.slow_raw);
        delete_if_present(files.slow_frames);
        fprintf("Native Mechanics Explorer videos and still frames are complete.\n");
    case "preview"
        capture_frame_stream( ...
            "1", 1, 10, [1280, 720], 11, ...
            files.preview_raw, files.preview_frames);
        encode_frame_stream(files.preview_frames, files.preview_video, 10);
        delete_if_present(files.preview_raw);
        delete_if_present(files.preview_frames);
        fprintf("Native Mechanics Explorer preview is complete.\n");
    case "capture_full"
        capture_frame_stream( ...
            "20", 1, 30, [1600, 900], 601, ...
            files.full_raw, files.full_frames);
    case "capture_slow"
        capture_frame_stream( ...
            "8", 0.5, 30, [1600, 900], 481, ...
            files.slow_raw, files.slow_frames);
end

clear cleanup_directory;
end

function files = output_files()
files.preview_raw = "mechanics_explorer_preview_native.avi";
files.preview_frames = "mechanics_explorer_preview_frames.mjpeg";
files.preview_video = "mechanics_explorer_preview.mp4";
files.full_raw = "mechanics_explorer_full_motion_native.avi";
files.full_frames = "mechanics_explorer_full_motion_frames.mjpeg";
files.full_video = "mechanics_explorer_full_motion.mp4";
files.slow_raw = "mechanics_explorer_first_swing_native.avi";
files.slow_frames = "mechanics_explorer_first_swing_frames.mjpeg";
files.slow_video = "mechanics_explorer_first_swing_slow_motion.mp4";
end

function capture_frame_stream( ...
    stop_time, playback_speed, frame_rate, frame_size, expected_frames, ...
    raw_name, frame_stream_name)
model_name = "inverted_pendulum_multibody";
if bdIsLoaded(model_name)
    close_system(model_name, false);
end
delete_if_present(raw_name);
delete_if_present(frame_stream_name);
load_system(model_name);
set_param(model_name, ...
    "SimMechanicsOpenEditorOnUpdate", "on", ...
    "StopTime", stop_time);

fprintf("Simulating %s seconds of Multibody motion.\n", stop_time);
sim(model_name);
smwritevideo( ...
    model_name, ...
    raw_name, ...
    "PlaybackSpeedRatio", playback_speed, ...
    "FrameRate", frame_rate, ...
    "VideoFormat", "motion jpeg avi", ...
    "FrameSize", frame_size);
fprintf("Waiting for %d native Mechanics Explorer frames.\n", expected_frames);
wait_for_frame_stream(raw_name, frame_stream_name, expected_frames);
end

function run_capture_process(project_directory, capture_mode, frame_stream_name)
delete_if_present(frame_stream_name);
matlab_executable = fullfile(matlabroot, "bin", "matlab");
matlab_command = sprintf( ...
    "cd('%s'); record_mechanics_explorer_videos('%s');", ...
    strrep(project_directory, "'", "''"), capture_mode);
command = sprintf( ...
    """%s"" -batch ""%s""", matlab_executable, matlab_command);
status = system(command);
if status ~= 0 && ~isfile(frame_stream_name)
    error("Mechanics Explorer capture process failed for mode '%s'.", capture_mode);
end
end

function wait_for_frame_stream(raw_name, frame_stream_name, expected_frames)
timeout_seconds = 900;
timer = tic;
while toc(timer) < timeout_seconds
    if isfile(raw_name)
        copyfile(raw_name, frame_stream_name, "f");
        frame_count = count_mjpeg_frames(frame_stream_name);
        if frame_count >= expected_frames
            fprintf("Captured %d native Mechanics Explorer frames.\n", frame_count);
            return;
        end
    end
    pause(2);
end
error("Timed out while waiting for native Mechanics Explorer frames.");
end

function frame_count = count_mjpeg_frames(filename)
ffprobe = find_command("ffprobe");
command = sprintf( ...
    """%s"" -v error -f mjpeg -count_frames -select_streams v:0 " + ...
    "-show_entries stream=nb_read_frames -of csv=p=0 ""%s"" 2>/dev/null", ...
    ffprobe, filename);
[status, output] = system(command);
if status == 0
    frame_count = str2double(strtrim(output));
    if isnan(frame_count)
        frame_count = 0;
    end
else
    frame_count = 0;
end
end

function encode_frame_stream(frame_stream_name, video_name, frame_rate)
ffmpeg = find_command("ffmpeg");
delete_if_present(video_name);
command = sprintf( ...
    """%s"" -y -v error -f mjpeg -framerate %d -i ""%s"" " + ...
    "-c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p " + ...
    "-movflags +faststart ""%s""", ...
    ffmpeg, frame_rate, frame_stream_name, video_name);
status = system(command);
if status ~= 0 || ~isfile(video_name)
    error("Unable to encode the native Mechanics Explorer frame stream.");
end
end

function command_path = find_command(command_name)
[status, output] = system("command -v " + command_name);
if status ~= 0
    error("Required command '%s' was not found.", command_name);
end
command_path = strtrim(output);
end

function save_still_frames(video_name)
save_video_frame(video_name, 0.1, "mechanics_explorer_start.png");
save_video_frame(video_name, 0.5, "mechanics_explorer_setup_overview.png");
save_video_frame(video_name, 2.75, "mechanics_explorer_first_swing.png");
save_video_frame(video_name, 10, "mechanics_explorer_mid_run.png");
save_video_frame(video_name, 19, "mechanics_explorer_late_motion.png");
end

function save_video_frame(video_name, frame_time, image_name)
reader = VideoReader(video_name);
reader.CurrentTime = min(frame_time, reader.Duration - 1 / reader.FrameRate);
frame = readFrame(reader);
imwrite(frame, image_name);
end

function delete_if_present(filename)
if isfile(filename)
    delete(filename);
end
end
