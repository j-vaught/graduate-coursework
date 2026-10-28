% A.5. Equal-temperament frequencies and note names.
clear; clc;

A4 = 440;                  % tuning reference, Hz
f = 1396.9;                % supplied frequency, Hz
n = round(12*log2(f/A4));  % nearest semitone from A4

E4 = A4*2^(-5/12);          % E4, five semitones below A4
F6 = A4*2^(20/12);        % F6, twenty semitones above A4
C0 = A4*2^(-57/12);        % lowest note shown in course-note chart
C10 = A4*2^(63/12);        % highest note shown in course-note chart
r = 2^(1/12);              % adjacent semitone frequency ratio

fprintf('E4 = %.6g Hz\n', E4);
fprintf('%.2f Hz is nearest to F6 (semitone offset from A4 = %d)\n', f, n);
fprintf('Course-note chart span: C0 = %.6g Hz to C10 = %.6g Hz\n', C0, C10);
fprintf('Nominal human hearing range = 20 Hz to 20 kHz\n');
fprintf('Equal temperament: 12 entries per octave; adjacent ratio = %.6g\n', r);
