function record_mechanics_explorer_videos(mode)
%RECORD_MECHANICS_EXPLORER_VIDEOS Record the native 3D model playback.

arguments
    mode (1, 1) string {mustBeMember(mode, ["all", "preview"])} = "all"
end

project_directory = fileparts(mfilename("fullpath"));
original_directory = pwd;
cleanup_directory = onCleanup(@() cd(original_directory));
cd(project_directory);

model_name = "inverted_pendulum_multibody";
if bdIsLoaded(model_name)
    close_system(model_name, false);
end
load_system(model_name);
set_param(model_name, "SimMechanicsOpenEditorOnUpdate", "on");
original_stop_time = string(get_param(model_name, "StopTime"));
cleanup_stop_time = onCleanup(@() set_param(model_name, "StopTime", original_stop_time));

if mode == "preview"
    delete_if_present("mechanics_explorer_preview.mp4");
    set_param(model_name, "StopTime", "1");
    sim(model_name);
    smwritevideo( ...
        model_name, ...
        "mechanics_explorer_preview.mp4", ...
        "PlaybackSpeedRatio", 1, ...
        "FrameRate", 10, ...
        "VideoFormat", "mpeg-4", ...
        "FrameSize", [1280, 720]);
    wait_for_video("mechanics_explorer_preview.mp4", 1);
else
    delete_if_present("mechanics_explorer_full_motion.mp4");
    delete_if_present("mechanics_explorer_first_swing_slow_motion.mp4");
    set_param(model_name, "StopTime", original_stop_time);
    sim(model_name);
    smwritevideo( ...
        model_name, ...
        "mechanics_explorer_full_motion.mp4", ...
        "PlaybackSpeedRatio", 1, ...
        "FrameRate", 30, ...
        "VideoFormat", "mpeg-4", ...
        "FrameSize", [1600, 900]);
    wait_for_video( ...
        "mechanics_explorer_full_motion.mp4", ...
        str2double(original_stop_time));

    set_param(model_name, "StopTime", "8");
    sim(model_name);
    smwritevideo( ...
        model_name, ...
        "mechanics_explorer_first_swing_slow_motion.mp4", ...
        "PlaybackSpeedRatio", 0.5, ...
        "FrameRate", 30, ...
        "VideoFormat", "mpeg-4", ...
        "FrameSize", [1600, 900]);
    wait_for_video("mechanics_explorer_first_swing_slow_motion.mp4", 16);

    save_video_frame( ...
        "mechanics_explorer_full_motion.mp4", 0.1, ...
        "mechanics_explorer_start.png");
    save_video_frame( ...
        "mechanics_explorer_full_motion.mp4", 2.75, ...
        "mechanics_explorer_first_swing.png");
    save_video_frame( ...
        "mechanics_explorer_full_motion.mp4", 10, ...
        "mechanics_explorer_mid_run.png");
    save_video_frame( ...
        "mechanics_explorer_full_motion.mp4", 19, ...
        "mechanics_explorer_late_motion.png");
end

clear cleanup_stop_time cleanup_directory;
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

function wait_for_video(filename, minimum_duration)
timeout_seconds = 600;
stable_checks_required = 4;
stable_checks = 0;
previous_size = -1;
timer = tic;

while toc(timer) < timeout_seconds
    if isfile(filename)
        file_info = dir(filename);
        if file_info.bytes == previous_size && file_info.bytes > 0
            stable_checks = stable_checks + 1;
        else
            stable_checks = 0;
            previous_size = file_info.bytes;
        end

        if stable_checks >= stable_checks_required
            try
                reader = VideoReader(filename);
                if reader.Duration >= minimum_duration - 0.2
                    return;
                end
            catch
                stable_checks = 0;
            end
        end
    end
    pause(1);
end

error("Timed out while waiting for Mechanics Explorer video '%s'.", filename);
end
