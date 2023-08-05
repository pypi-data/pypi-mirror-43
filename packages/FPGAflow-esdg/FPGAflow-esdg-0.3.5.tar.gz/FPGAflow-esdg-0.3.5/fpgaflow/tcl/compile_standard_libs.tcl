set simulator_name [lindex $argv 0]
set simulator_exec_path [lindex $argv 1]
set output_path [lindex $argv 2]
set arch64 [lindex $argv 3]

puts "simulator_name=${simulator_name}"
puts "simulator_exec_path=${simulator_exec_path}"
puts "output_path=${output_path}"
puts "arch64=${arch64}"

set_param general.maxThreads 8

if { $arch64 } {
    compile_simlib -force \
        -language all \
        -simulator ${simulator_name} \
        -verbose  \
        -library all \
        -family  all \
        -no_ip_compile \
        -simulator_exec_path ${simulator_exec_path} \
        -directory ${output_path}
} else {
    compile_simlib -force \
        -language all \
        -simulator ${simulator_name} \
        -32bit \
        -verbose  \
        -library all \
        -family  all \
        -no_ip_compile \
        -simulator_exec_path ${simulator_exec_path} \
        -directory ${output_path}
}
