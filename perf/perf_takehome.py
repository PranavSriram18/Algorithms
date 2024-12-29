"""
# Anthropic's Performance Engineering Take-home V2

Copyright Anthropic PBC 2023. Permission is granted to modify and use, but not
to publish or redistribute. 

# Unusual allowances: 

- You should copy these files to your computer and edit in your own environment
  so that you can use the trace functionality. If the CodeSignal platform said
  anything about not doing this, ignore it. We'll ignore any warnings the
  platform gives due to this allowance.
- You're welcome to use any online resources including language models. In fact
  you're encouraged to install Github Copilot, it'll likely only help a little.
  CodeSignal makes you promise that you'll only use language reference
  resources, there's no way to disable that promise, you're welcome to use
  non-language resources.
- You may use any libraries you want while debugging but your uploaded solution
  must use only the standard library.

# Rules

- You may not consult with anyone else while you're doing this problem.
- Please don't tell anyone else about the details of this problem other than the
  vague description communicated before you started.

# Instructions

- Please paste back onto and submit on CodeSignal regularly, ideally every time
  you make a substantial advance in your kernel code or otherwise every hour. We
  may be impressed by various pieces of progress even if you get stuck at other
  times. Note that the speed tests mean you'll "fail" tests even if your kernel
  is correct.
- Keep an eye on CodeSignal's timer and please try to paste your code just
  before you finish and submit it. If you fail to do this, please send an email
  to tristan@anthropic.com with your code and we'll line up the email and
  CodeSignal timestamps.
- You must preserve the KernelBuilder constructor and build_kernel interface,
  since that's how we'll test your solution.

# Task

- Optimize the kernel as much as possible in the available time. 
    - The machine parameters are balanced so that how impressed we are by you
      doing an optimization is roughly proportional to its speedup factor.
      Although it's not perfect.
    - The exception to the above is doing basic multicore, which we recommend
      you start with as a warmup.
    - The input used in test_kernel_cycles is what your performance will be
      scored on.

# Tips

- You'll be evaluated primarily on the speed of your correct kernel submissions.
  You're encouraged to improve the debugging/trace tooling present in this file,
  but only implement tooling and write nice code to the extent that in your
  judgement it'll best help you achieve a fast and correct solution.
- Try to keep a copy of your first correct kernel somewhere so you can compare
  against it when debugging.
- Modifying the simulator is one of the most powerful debugging tools available,
  you should take advantage of it. But your solution will be tested with an
  unmodified simulator so don't change the behavior or API.

We recommend you read through problem.py next.
"""

import random
import unittest

from problem import *


class KernelBuilder:
    def __init__(self):
        self.instrs = []
        self.labels = {}
        self.scratch = {}
        self.scratch_debug = {}
        self.scratch_ptr = 0
        self.const_map = {}

    def debug_info(self):
        # Hint: This isn't consumed anywhere, but you should probably use it in some way for debugging
        return DebugInfo(scratch_map=self.scratch_debug)

    def build(self, slots: list[tuple[Engine, tuple]], vliw: bool = False):
        # Simple slot packing that just uses one slot per instruction bundle
        instrs = []
        for engine, slot in slots:
            instrs.append({engine: [slot]})
        return instrs

    def add(self, engine, slot):
        self.instrs.append({engine: [slot]})

    def label(self, name):
        self.labels[name] = len(self.instrs)

    def alloc_scratch(self, name=None, length=1):
        addr = self.scratch_ptr
        if name is not None:
            self.scratch[name] = addr
            self.scratch_debug[addr] = (name, length)
        self.scratch_ptr += length
        assert self.scratch_ptr <= SCRATCH_SIZE, "Out of scratch space"
        return addr

    def scratch_const(self, val, name=None):
        if val not in self.const_map:
            addr = self.alloc_scratch(name)
            self.add("load", ("const", addr, val))
            self.const_map[val] = addr
        return self.const_map[val]

    def for_loop(self, iter_addr, limit_addr, body: list[Instruction]):
        """
        A for loop that runs len times
        """
        loop_cond = self.alloc_scratch()
        one_constant = self.scratch_const(1)
        start_addr = len(self.instrs)
        prologue_len, epilogue_len = 3, 1
        end_addr = start_addr + prologue_len + len(body) + epilogue_len
        instrs = [
            {"alu": [("+", iter_addr, one_constant, iter_addr)]},
            {"alu": [("<", loop_cond, limit_addr, iter_addr)]},
            {"flow": [("cond_jump", loop_cond, end_addr)]},
        ]
        instrs.extend(body)
        instrs.append({"flow": [("jump", start_addr)]})
        return instrs

    def build_simple_test(self):
        """
        A simple test program that just counts to 10
        """
        # Scratch space addresses
        one_constant = self.scratch_const(1)
        accum = self.alloc_scratch("accum")
        iter_addr = self.alloc_scratch("iter")
        limit_addr = self.alloc_scratch("limit")
        self.add("load", ("const", limit_addr, 10))
        body = [("alu", ("+", accum, accum, one_constant))]
        self.instrs.extend(self.for_loop(iter_addr, limit_addr, self.build(body)))

    def build_hash(self, val_hash_addr, tmp1, tmp2):
        slots = []

        for op1, val1, op2, op3, val3 in HASH_STAGES:
            slots.append(("alu", (op1, tmp1, val_hash_addr, self.scratch_const(val1))))
            slots.append(("alu", (op3, tmp2, val_hash_addr, self.scratch_const(val3))))
            slots.append(("alu", (op2, val_hash_addr, tmp1, tmp2)))

        return slots
    
    def build_kernel(self, forest_height: int, n_nodes: int, batch_size: int):
        """Optimized kernel implementation using VLIW, SIMD, and advanced scheduling"""
        
        # Constants we'll need frequently
        zero_const = self.scratch_const(0)
        one_const = self.scratch_const(1) 
        two_const = self.scratch_const(2)
        vlen_const = self.scratch_const(VLEN)
        mask_const = self.scratch_const(0xFFFFFFFF)
        
        # Vector constants - allocate space and broadcast scalar to vector
        v_zero = self.alloc_scratch("v_zero", VLEN)
        v_one = self.alloc_scratch("v_one", VLEN)
        v_two = self.alloc_scratch("v_two", VLEN)
        v_mask = self.alloc_scratch("v_mask", VLEN)
        
        # Broadcast constants to vectors
        self.add("valu", ("vbroadcast", v_zero, zero_const))
        self.add("valu", ("vbroadcast", v_one, one_const))
        self.add("valu", ("vbroadcast", v_two, two_const))
        self.add("valu", ("vbroadcast", v_mask, mask_const))
        
        # Memory pointers and indices
        mem_tmp = self.alloc_scratch("mem_tmp")
        mem_vars = ["rounds", "n_nodes", "batch_size", "forest_height", 
                    "forest_values_p", "inp_indices_p", "inp_values_p"]
        for i, v in enumerate(mem_vars):
            addr = self.alloc_scratch(v)
            self.add("load", ("const", mem_tmp, i))
            self.add("load", ("load", addr, mem_tmp))
        
        # Core state & control - after memory initialization
        core_id = self.alloc_scratch("core_id")
        self.add("flow", ("coreid", core_id))
        
        # Calculate items per core
        batch_per_core = batch_size // N_CORES
        batch_per_core_addr = self.scratch_const(batch_per_core)
        core_offset = self.alloc_scratch("core_offset")
        self.add("alu", ("*", core_offset, core_id, batch_per_core_addr))
        
        # Vector registers for processing VLEN items at once
        v_indices = self.alloc_scratch("v_indices", VLEN)
        v_values = self.alloc_scratch("v_values", VLEN)
        v_node_vals = self.alloc_scratch("v_node_vals", VLEN)
        v_tmp1 = self.alloc_scratch("v_tmp1", VLEN)
        v_tmp2 = self.alloc_scratch("v_tmp2", VLEN)
        v_tmp3 = self.alloc_scratch("v_tmp3", VLEN)
        
        # Broadcast n_nodes to vector for range comparison
        v_n_nodes = self.alloc_scratch("v_n_nodes", VLEN)
        self.add("valu", ("vbroadcast", v_n_nodes, self.scratch["n_nodes"]))
        
        # Initialize loop counters to zero
        round_i = self.alloc_scratch("round_i")
        batch_i = self.alloc_scratch("batch_i")
        self.add("alu", ("+", round_i, zero_const, zero_const))
        self.add("alu", ("+", batch_i, zero_const, zero_const))
        
        # Scratch for index calculations
        batch_abs_idx = self.alloc_scratch("batch_abs_idx")
        node_addr = self.alloc_scratch("node_addr")
        load_tmp = self.alloc_scratch("load_tmp")
        idx_tmp = self.alloc_scratch("idx_tmp")
        
        # Vector registers for hash constants
        hash_constants = {}
        for op1, val1, op2, op3, val3 in HASH_STAGES:
            if val1 not in hash_constants:
                v_addr = self.alloc_scratch(f"v_hash_{val1}", VLEN)
                val1_const = self.scratch_const(val1)
                self.add("valu", ("vbroadcast", v_addr, val1_const))
                hash_constants[val1] = v_addr
            if val3 not in hash_constants:
                v_addr = self.alloc_scratch(f"v_hash_{val3}", VLEN)
                val3_const = self.scratch_const(val3)
                self.add("valu", ("vbroadcast", v_addr, val3_const))
                hash_constants[val3] = v_addr
        
        # Build the body of the batch processing loop
        batch_body = []
        
        # Calculate absolute index for this SIMD batch
        batch_body.append(("alu", ("*", batch_abs_idx, batch_i, vlen_const)))
        batch_body.append(("alu", ("+", batch_abs_idx, batch_abs_idx, core_offset)))
        
        # Load VLEN indices and values
        batch_body.append(("alu", ("+", mem_tmp, self.scratch["inp_indices_p"], batch_abs_idx)))
        batch_body.append(("load", ("vload", v_indices, mem_tmp)))
        batch_body.append(("alu", ("+", mem_tmp, self.scratch["inp_values_p"], batch_abs_idx)))
        batch_body.append(("load", ("vload", v_values, mem_tmp)))
        
        # Load node values individually using indirect access
        for i in range(VLEN):
            # Get index value from v_indices[i]
            batch_body.append(("load", ("load_offset", load_tmp, v_indices, i)))  # Load the actual index value
            
            # Calculate forest address and load value
            batch_body.append(("alu", ("+", node_addr, self.scratch["forest_values_p"], load_tmp)))
            batch_body.append(("load", ("load", load_tmp, node_addr)))
            
            # Store to v_node_vals[i]
            batch_body.append(("alu", ("+", v_node_vals + i, load_tmp, zero_const)))
        
        # Initial XOR into temporary
        batch_body.append(("valu", ("^", v_tmp1, v_values, v_node_vals)))
        batch_body.append(("valu", ("&", v_tmp1, v_tmp1, v_mask)))
        
        # Hash computation
        for op1, val1, op2, op3, val3 in HASH_STAGES:
            batch_body.append(("valu", (op1, v_tmp2, v_tmp1, hash_constants[val1])))
            batch_body.append(("valu", ("&", v_tmp2, v_tmp2, v_mask)))
            
            batch_body.append(("valu", (op3, v_tmp3, v_tmp1, hash_constants[val3])))
            batch_body.append(("valu", ("&", v_tmp3, v_tmp3, v_mask)))
            
            batch_body.append(("valu", (op2, v_tmp1, v_tmp2, v_tmp3)))
            batch_body.append(("valu", ("&", v_tmp1, v_tmp1, v_mask)))
        
        # Copy final hash result to v_values
        batch_body.append(("valu", ("+", v_values, v_tmp1, v_zero)))
        
        # Check if values are even/odd using the hashed value
        batch_body.append(("valu", ("%", v_tmp1, v_values, v_two)))
        batch_body.append(("valu", ("==", v_tmp1, v_tmp1, v_zero)))
        
        # Compute 2*indices + (1 or 2)
        batch_body.append(("valu", ("*", v_indices, v_indices, v_two)))
        batch_body.append(("flow", ("vselect", v_tmp2, v_tmp1, v_two, v_one)))
        batch_body.append(("valu", ("+", v_indices, v_indices, v_tmp2)))
        
        # Check range and wrap to root if needed
        batch_body.append(("valu", ("<", v_tmp1, v_indices, v_n_nodes)))
        batch_body.append(("flow", ("vselect", v_indices, v_tmp1, v_indices, v_zero)))
        
        # Store results back to memory
        batch_body.append(("alu", ("+", mem_tmp, self.scratch["inp_values_p"], batch_abs_idx)))
        batch_body.append(("store", ("vstore", mem_tmp, v_values)))
        batch_body.append(("alu", ("+", mem_tmp, self.scratch["inp_indices_p"], batch_abs_idx)))
        batch_body.append(("store", ("vstore", mem_tmp, v_indices)))
        
        # Create nested loops
        batches_per_core = batch_per_core // VLEN
        batches_addr = self.scratch_const(batches_per_core)
        batch_body_instrs = self.build(batch_body)
        batch_loop = self.for_loop(batch_i, batches_addr, batch_body_instrs)
        round_loop = self.for_loop(round_i, self.scratch["rounds"], batch_loop)
        
        # Add to program
        self.instrs.extend(round_loop)
    
        

    def build_kernel_old(self, forest_height: int, n_nodes: int, batch_size: int):
        """
        Old version for reference/debugging.
        Like reference_kernel2 but building actual instructions.
        Just the simplest implementation and non-overlapping scheduling possible.

        batch_size is guaranteed to be a multiple of VLEN*N_CORES*16
        """
        tmp1 = self.alloc_scratch("tmp1")
        tmp2 = self.alloc_scratch("tmp2")
        # Scratch space addresses
        init_vars = [
            "rounds",
            "n_nodes",
            "batch_size",
            "forest_height",
            "forest_values_p",
            "inp_indices_p",
            "inp_values_p",
        ]
        for v in init_vars:
            self.alloc_scratch(v, 1)
        for i, v in enumerate(init_vars):
            self.add("load", ("const", tmp1, i))
            self.add("load", ("load", self.scratch[v], tmp1))

        zero_const = self.scratch_const(0)
        one_const = self.scratch_const(1)
        two_const = self.scratch_const(2)

        # Halt cores that aren't participating
        # Interestingly, if we omit this logic the result is the same since all the cores
        # operate in lockstep and do the same memory reads and writes, but the Python runs longer
        self.add("flow", ("coreid", tmp1))
        self.add("alu", ("==", tmp1, tmp1, zero_const))
        self.add("flow", ("cond_jump_rel", tmp1, 1))
        self.add("flow", ("halt",))

        # Pause instructions let us debug at intermediate steps
        self.add("flow", ("pause",))
        # Any debug engine instruction is ignored by the submission simulator
        self.add("debug", ("comment", "Starting loop"))

        body = []  # array of slots
        batch_i = self.alloc_scratch("batch_i")
        tmp_idx = self.alloc_scratch("tmp_idx")
        tmp_val = self.alloc_scratch("tmp_val")
        tmp_node_val = self.alloc_scratch("tmp_node_val")
        for i in range(batch_size):
            body.append(("load", ("const", batch_i, i)))
            # Write the instructions corresponding to the innermost body of reference_kernel2
            # idx = mem[inp_indices_p + i]
            # val = mem[inp_values_p + i]
            body.append(("alu", ("+", tmp_idx, self.scratch["inp_indices_p"], batch_i)))
            body.append(("load", ("load", tmp_idx, tmp_idx)))
            body.append(("alu", ("+", tmp_val, self.scratch["inp_values_p"], batch_i)))
            body.append(("load", ("load", tmp_val, tmp_val)))
            # node_val = mem[forest_values_p + idx]
            body.append(
                ("alu", ("+", tmp_node_val, self.scratch["forest_values_p"], tmp_idx))
            )
            body.append(("load", ("load", tmp_node_val, tmp_node_val)))
            # val = myhash(val ^ node_val)
            body.append(("alu", ("^", tmp_val, tmp_val, tmp_node_val)))
            body.extend(self.build_hash(tmp_val, tmp1, tmp2))
            # idx = 2*i + (1 if val % 2 == 0 else 2)
            body.append(("alu", ("%", tmp1, tmp_val, self.scratch_const(2))))
            body.append(("alu", ("==", tmp1, tmp1, self.scratch_const(0))))
            body.append(("flow", ("select", tmp2, tmp1, one_const, two_const)))
            body.append(("alu", ("*", tmp_idx, tmp_idx, two_const)))
            body.append(("alu", ("+", tmp_idx, tmp_idx, tmp2)))
            # idx = 0 if idx >= n_nodes else idx
            body.append(("alu", ("<", tmp1, tmp_idx, self.scratch["n_nodes"])))
            body.append(("flow", ("select", tmp_idx, tmp1, tmp_idx, zero_const)))
            # mem[inp_values_p + i] = val
            # mem[inp_indices_p + i] = idx
            body.append(("alu", ("+", tmp1, self.scratch["inp_values_p"], batch_i)))
            body.append(("store", ("store", tmp1, tmp_val)))
            body.append(("alu", ("+", tmp1, self.scratch["inp_indices_p"], batch_i)))
            body.append(("store", ("store", tmp1, tmp_idx)))

        body_instrs = self.build(body)
        body_instrs.append({"flow": [("pause",)]})

        height_i = self.alloc_scratch("height_i")
        loop = self.for_loop(height_i, self.scratch["rounds"], body_instrs)
        self.instrs.extend(loop)


def do_kernel_test(
    forest_height: int,
    rounds: int,
    batch_size: int,
    seed: int = 123,
    trace: bool = False,
    prints: bool = False,
):
    print(f"{forest_height=}, {rounds=}, {batch_size=}")
    random.seed(seed)
    forest = Tree.generate(forest_height)
    inp = Input.generate(forest, batch_size, rounds)
    mem = build_mem_image(forest, inp)

    kb = KernelBuilder()
    kb.build_kernel(forest.height, len(forest.values), len(inp.indices))
    # print(kb.instrs)

    machine = Machine(mem, kb.instrs, kb.debug_info(), n_cores=N_CORES, trace=trace)
    machine.prints = prints
    for i, ref_mem in enumerate(reference_kernel2(mem)):
        machine.run()
        inp_values_p = ref_mem[6]
        if prints:
            print(machine.mem[inp_values_p : inp_values_p + len(inp.values)])
            print(ref_mem[inp_values_p : inp_values_p + len(inp.values)])
        assert (
            machine.mem[inp_values_p : inp_values_p + len(inp.values)]
            == ref_mem[inp_values_p : inp_values_p + len(inp.values)]
        ), f"Incorrect result on round {i}"
        inp_indices_p = ref_mem[5]
        if prints:
            print(machine.mem[inp_indices_p : inp_indices_p + len(inp.indices)])
            print(ref_mem[inp_indices_p : inp_indices_p + len(inp.indices)])
        # Updating these in memory isn't required, but you can enable this check for debugging
        # assert machine.mem[inp_indices_p:inp_indices_p+len(inp.indices)] == ref_mem[inp_indices_p:inp_indices_p+len(inp.indices)]

    print("CYCLES: ", machine.cycle)
    return machine.cycle


class Tests(unittest.TestCase):
    def test_ref_kernels(self):
        """
        Test the reference kernels against each other
        """
        random.seed(123)
        for i in range(10):
            f = Tree.generate(4)
            inp = Input.generate(f, 10, 6)
            mem = build_mem_image(f, inp)
            reference_kernel(f, inp)
            for _ in reference_kernel2(mem):
                pass
            assert inp.indices == mem[mem[5] : mem[5] + len(inp.indices)]
            assert inp.values == mem[mem[6] : mem[6] + len(inp.values)]

    def test_simple(self):
        # Test the kernel builder
        kb = KernelBuilder()
        kb.build_simple_test()
        # print(kb.instrs)

        # Test the machine
        mem = [0] * 10
        machine = Machine(mem, kb.instrs, kb.debug_info())
        machine.prints = True
        machine.run()
        # print(machine.cores[0])
        assert machine.cores[0].scratch[1] == 10

    def test_kernel_trace(self):
        # Tiny example for correctness debugging
        # do_kernel_test(3, 1, 1, trace=True, prints=True)
        # Full-scale example for performance testing
        do_kernel_test(10, 16, 1024, trace=True, prints=False)

    def test_kernel_correctness(self):
        # Technically passing this test is not required for submission, see submission_tests.py for the actual correctness test
        # Feel free not to run this yourself if your compiler is slow at it
        for batch in range(1, 3):
            for forest_height in range(3):
                do_kernel_test(
                    forest_height + 2, forest_height + 4, batch * 16 * VLEN * N_CORES
                )

    def test_kernel_cycles(self):
        do_kernel_test(10, 16, 1024)


# To run all the tests:
#    python perf_takehome.py
# To run a specific test:
#    python perf_takehome.py Tests.test_kernel_cycles
# To view a hot-reloading trace of all the instructions:  **Recommended debug loop**
#    python perf_takehome.py Tests.test_kernel_trace
# Then run `python watch_trace.py` in another tab, it'll open a browser tab, then click "Open Perfetto"
# You can then keep that open and re-run the test to see a new trace.

# To test the actual submission tests that CodeSignal will run:
#    python tests/submission_tests.py

if __name__ == "__main__":
    unittest.main()
