function create_simplified_multibody_model
%CREATE_SIMPLIFIED_MULTIBODY_MODEL Create a clean, editable presentation copy.

source_model = "inverted_pendulum_multibody";
output_model = "inverted_pendulum_multibody_simplified";

if bdIsLoaded(output_model)
    close_system(output_model, 0);
end

load_system(source_model);
save_system(source_model, output_model + ".slx");

blocks_to_remove = [
    "Convert x"
    "Convert theta"
    "x to workspace"
    "theta to workspace"
];

for index = 1:numel(blocks_to_remove)
    block_path = output_model + "/" + blocks_to_remove(index);
    if getSimulinkBlockHandle(block_path) ~= -1
        delete_connected_lines(block_path);
        delete_block(block_path);
    end
end

set_param(output_model + "/Cart translation", "SensePosition", "off");
set_param(output_model + "/Damped pivot", "SensePosition", "off");

set_param(output_model + "/World Frame", ...
    "Position", [40, 240, 100, 300]);
set_param(output_model + "/Gravity", ...
    "Position", [40, 75, 135, 135]);
set_param(output_model + "/Solver Configuration", ...
    "Position", [40, 405, 135, 465]);
set_param(output_model + "/Align cart axis", ...
    "Position", [150, 235, 235, 305], ...
    "Name", "Cart axis");
set_param(output_model + "/Cart translation", ...
    "Position", [285, 225, 390, 315]);
set_param(output_model + "/Cart mass", ...
    "Position", [435, 75, 545, 145]);
set_param(output_model + "/Align pivot axis", ...
    "Position", [440, 235, 535, 305], ...
    "Name", "Pivot axis");
set_param(output_model + "/Damped pivot", ...
    "Position", [585, 225, 690, 315]);
set_param(output_model + "/Pendulum length", ...
    "Position", [740, 235, 835, 305], ...
    "Name", "Pendulum rod");
set_param(output_model + "/Pendulum point mass", ...
    "Position", [890, 235, 1010, 305]);

set_param(output_model, "Location", [80, 80, 1350, 720]);
save_system(output_model);
open_system(output_model);
set_param(output_model, "ZoomFactor", "FitSystem");
end

function delete_connected_lines(block_path)
line_handles = get_param(block_path, "LineHandles");
port_groups = fieldnames(line_handles);
for group_index = 1:numel(port_groups)
    handles = unique(line_handles.(port_groups{group_index}));
    handles = handles(handles ~= -1);
    for handle_index = 1:numel(handles)
        delete_line(handles(handle_index));
    end
end
end
