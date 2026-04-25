from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
import numpy as np

# ===============================
# 五声权重（前置音 v0）
# ===============================
weights = {
    "000": 0.08,  # 宫
    "001": 0.62,  # 商
    "011": 0.08,  # 徵
    "100": 0.22   # 羽
}

n_qubits = 3

# ===============================
# 构造初态 |s_w>
# ===============================
def build_initial_state():
    dim = 2**n_qubits
    state = np.zeros(dim, dtype=complex)

    for bitstr, w in weights.items():
        idx = int(bitstr, 2)
        state[idx] = np.sqrt(w)

    # 归一化（理论上已归一）
    state = state / np.linalg.norm(state)
    return state


# ===============================
# 构造相位预言机 U_f
# ===============================
def phase_oracle():
    qc = QuantumCircuit(n_qubits)

    for bitstr, w in weights.items():
        theta = np.pi * w
        idx = int(bitstr, 2)

        # 将目标态映射到 |111>
        for i in range(n_qubits):
            if bitstr[i] == '0':
                qc.x(i)

        # 多控制相位（用 mcp）
        qc.mcp(theta, [0,1], 2)

        # 还原
        for i in range(n_qubits):
            if bitstr[i] == '0':
                qc.x(i)

    return qc


# ===============================
# 构造扩散算子 U_phi
# ===============================
def diffusion_operator(initial_state):
    qc = QuantumCircuit(n_qubits)

    # A†
    qc.initialize(initial_state, range(n_qubits))
    qc.inverse()

    # 对 |000> 做相位翻转
    qc.h(n_qubits-1)
    qc.mcx([0,1], 2)
    qc.h(n_qubits-1)

    # A
    qc.initialize(initial_state, range(n_qubits))

    return qc


# ===============================
# 主电路
# ===============================
def nrt_quantum_circuit():
    qc = QuantumCircuit(n_qubits, n_qubits)

    # 初态
    init_state = build_initial_state()
    qc.initialize(init_state, range(n_qubits))
    qc.barrier()

    # 相位预言机
    qc.compose(phase_oracle(), inplace=True)
    qc.barrier()

    # 扩散算子
    qc.compose(diffusion_operator(init_state), inplace=True)
    qc.barrier()

    # 测量
    qc.measure(range(n_qubits), range(n_qubits))

    return qc


# ===============================
# 仿真（IBM Aer）
# ===============================
if __name__ == "__main__":
    qc = nrt_quantum_circuit()

    simulator = AerSimulator()
    compiled = transpile(qc, simulator)
    result = simulator.run(compiled, shots=2048).result()

    counts = result.get_counts()

    print("=== 测量结果 ===")
    print(counts)

    print("\n=== 电路结构 ===")
    print(qc.draw(fold=-1))
